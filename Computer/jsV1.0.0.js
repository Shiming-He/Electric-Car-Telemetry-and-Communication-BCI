/* 
V1.0 
jsV1.0.0.js
@author Shiming He 
Original Author: Austin Wang
2023-05-13
Created to be able to be used with the new generation telementery and Communication System
*/
// Set this value depending on the battery
var dataAhLeft = 0;
var total_Ah = 0;
var remaining_time = 0;
var ah_used_min = 0;
var perdict_target_ah = 0;

/* Variable initializations including channel and entry*/
var dataAh = 0;
var dataV = 0;
var dataA = 0;
var dataS = 0;
var dataD = 0;
/* variables for finding mean of the the three variable, to test if it would remove noice*/
/* Ah resets this will still repersent the total value*/
var dataAhPast = 0;
var dataAhPastTotal = 0;
var dataAhTotal = 0; 

var dataVTotal = 0;
var amountDataAdded = 0;

var button_val = false;


// set the message information for the site
const messagesSystemTop = document.getElementById('messagesSystem');
const messagesRawDataTop = document.getElementById('messagesRawData');
const messagesProcessedDataBottom = document.getElementById('messagesProcessedData');
const messagesAhLeftTop = document.getElementById('messagesAhLeft');

// set the PubNub Channel and Entry
const theChannel = 'the_guide';
const theEntry = 'Earth';


/* Make a pubnub object, define keys and open connection */
const pubnub = new PubNub({
  publishKey: 'pub-c-f418f6ca-711a-402a-b373-fe542788cf3b',//use your PubNub publish key
  subscribeKey: 'sub-c-3a2983ca-ce37-11ec-ab76-de5c934881d6', // use your PubNub subscribe key
  uuid: "theClientUUID"
});
pubnub.subscribe({
  channels: ['the_guide'],
  withPresence: true
});


/*Listen for messages */
pubnub.addListener({

  message: function(event) {
    var messageIn = event.message.update;
    var messageEntry = event.message.entry;

    if (messageIn == "PN Connected") {
      displaySystemMessage('[MESSAGE: received]',
      messageEntry + ': ' + messageIn);
    } else if (messageIn == 'Harmless.'){
      displaySystemMessage('[MESSAGE: received]',
      messageEntry + ': ' + messageIn);
    } else {
      // check to make sure the message is not from the computer (Houtson)
      // if it is make sure do not print or look through the message 
      if (messageEntry != 'Houston'){
          onReceive(messageIn);
      }
    }
  },

  presence: function(event) {
    displaySystemMessage('[PRESENCE: ' + event.action + ']',
    'uuid: ' + event.uuid + ', channel: ' + event.channel);
  },

  status: function(event) {
    displaySystemMessage('[STATUS: ' + event.category + ']',
    'connected to channels: ' + event.affectedChannels);

    if (event.category == 'PNConnectedCategory') {
      submitUpdate(theEntry, 'PN Connected');
    }    
  } 

});


/* Update for system messages */
submitUpdate = function(anEntry, anUpdate) {
  pubnub.publish({
    channel : theChannel,
    message : {'entry' : anEntry, 'update' : anUpdate}
  },
  function(status, response) {
    if (status.error) {
      console.log(status)
    }
    else {
      displaySystemMessage('[PUBLISH: sent]',
      'timetoken: ' + response.timetoken);
    }
  });
};


/* Output system messages in the messagesSystem div */
displaySystemMessage = function(messageType, aMessage) {
  let pMessage = document.createElement('p');
  let br = document.createElement('br');

  messagesSystemTop.after(pMessage);
  pMessage.appendChild(document.createTextNode(messageType));
  pMessage.appendChild(br);
  pMessage.appendChild(document.createTextNode(aMessage));
}


/* Output data messages in the messagesRawData div */
displayRawDataIn = function(lastIn) {
  let p = document.createElement('p');

  messagesRawDataTop.after(p);
  p.appendChild(document.createTextNode(lastIn));
} 
/* Output data messages in the messagesProcessedData div */
displayProcessedDataIn = function(lastIn) {
  let p = document.createElement('p');

  messagesProcessedDataBottom.after(p);
  p.appendChild(document.createTextNode(lastIn));
} 

/* Output data messages in the Ah Left Column div */
perdictDataAhIn = function(AhLeft, AhPastMin) {
  let p = document.createElement('p');
  let br = document.createElement('br');

  messagesAhLeftTop.after(p);
  p.appendChild(document.createTextNode(AhLeft));
  p.appendChild(document.createTextNode(',  '));
  p.appendChild(document.createTextNode(AhPastMin));
} 
 
/*
Upon msg receival
*/
function onReceive(messageIn) {
  const myArray = messageIn.trim().split(/\s+/);
  // check what message it is
 
  if (myArray.length >= 1 && myArray[0] == 'raw'){ //if it is a raw message
      
      displayRawDataIn(messageIn);
      
      if (myArray.length == 6 && myArray[1] != 'blank'){
          //Ah
          dataAh = parseFloat(myArray[1]);
          //V
          dataVTotal = parseFloat(myArray[2]);

          amountDataAdded ++;
          if (amountDataAdded == 5) {
              dataV =  dataVTotal/5;
              amountDataAdded = 0;
              dataVTotal = 0;
          }
          //A
          dataA = parseFloat(myArray[3]);
          //S
          dataS = parseFloat(myArray[4]);
          //D
          dataD = parseFloat(myArray[5]);
      }
  }
    
  if (myArray.length == 6 && myArray[0] == 'prep'){// if it is a processed message
      displayProcessedDataIn(messageIn);
      
      // total Ah
      total_Ah = parseFloat(myArray[1]);
      
      // Ah Left
      dataAhLeft = parseFloat(myArray[2]);
      
      // Remaining Time
      remaining_time = parseFloat(myArray[3]);
      
      
      ah_used_min = parseFloat(myArray[4]);
      perdict_target_ah = parseFloat(myArray[5]);
      perdictDataAhIn(perdict_target_ah, ah_used_min);
  }
}


/*
Graphs Ah and V data
*/
function getTime() {
  d = new Date();
  return d;
}


/* Ah graph */      
var layout1 = {
  title: {
    text:'Amp-hours vs. Time',
  },
  xaxis: {
    title: {
      text: 'Time',
    },
    type: 'date'
  },
  yaxis: {
    title: {
      text: 'Amp-hours (Ah)',
    }
  }
};

var trace1 = {
  x: [getTime()],
  y: [dataAh],
  type: 'line'
};

var data1 = [trace1];
Plotly.plot('chartAh',data1,layout1);

setInterval(function(){
  Plotly.extendTraces('chartAh',{x:[[getTime()]], y:[[dataAh]]}, [0]);
}, 1000);




/* V graph */  
var layout2 = {
  title: {
    text:'Voltage vs. Time',
  },

  xaxis: {
    title: {
      text: 'Time',
    },
    type: 'date'
  },
  yaxis: {
    title: {
      text: 'Voltage (V)',
    }
  }
};

var trace2 = {
  x: [getTime()],
  y: [dataV],
  type: 'line'
};

var data2 = [trace2];
Plotly.plot('chartV',data2, layout2);

setInterval(function(){
  Plotly.extendTraces('chartV',{x:[[getTime()]], y:[[dataV]]}, [0]);
}, 1000);



/* Amperage graph */  
var layout3 = {
  title: {
    text:'Amperage vs. Time',
  },

  xaxis: {
    title: {
      text: 'Time',
    },
    type: 'date'
  },
  yaxis: {
    title: {
      text: 'Amperage',
    }
  }
};

var trace3 = {
  x: [getTime()],
  y: [dataA],
  type: 'line'
};

var data3 = [trace3];
Plotly.plot('chartA',data3, layout3);

setInterval(function(){
  Plotly.extendTraces('chartA',{x:[[getTime()]], y:[[dataA]]}, [0]);
}, 1000);





/* Speed graph */  
var layout4 = {
  title: {
    text:'Speed vs. Time',
  },

  xaxis: {
    title: {
      text: 'Time',
    },
    type: 'date'
  },
  yaxis: {
    title: {
      text: 'Speed',
    }
  }
};

var trace4 = {
  x: [getTime()],
  y: [dataS],
  type: 'line'
};

var data4 = [trace4];
Plotly.plot('chartS',data4, layout4);

setInterval(function(){
  Plotly.extendTraces('chartS',{x:[[getTime()]], y:[[dataS]]}, [0]);
}, 1000);




/* D graph */  
var layout5 = {
  title: {
    text:'Distance vs. Time',
  },

  xaxis: {
    title: {
      text: 'Time',
    },
    type: 'date'
  },
  yaxis: {
    title: {
      text: 'D3',
    }
  }
};

var trace5 = {
  x: [getTime()],
  y: [dataD],
  type: 'line'
};

var data5 = [trace5];
Plotly.plot('chartD',data5, layout5);

setInterval(function(){
  Plotly.extendTraces('chartD',{x:[[getTime()]], y:[[dataD]]}, [0]);
}, 1000);





/* Total Ah graph */  
var layout6 = {
  title: {
    text:'Total Ah vs. Time',
  },

  xaxis: {
    title: {
      text: 'Time',
    },
    type: 'date'
  },
  yaxis: {
    title: {
      text: 'Ah',
    }
  }
};

var trace6 = {
  x: [getTime()],
  y: [total_Ah],
  type: 'line'
};

var data6 = [trace6];
Plotly.plot('chartTotalAh',data6, layout6);

setInterval(function(){
  Plotly.extendTraces('chartTotalAh',{x:[[getTime()]], y:[[total_Ah]]}, [0]);
}, 1000);





/* Ah used in last minute graph */  
var layout7 = {
  title: {
    text:'Ah used in last min vs. Time',
  },

  xaxis: {
    title: {
      text: 'Time',
    },
    type: 'date'
  },
  yaxis: {
    title: {
      text: 'Ah/min',
    }
  }
};

var trace7 = {
  x: [getTime()],
  y: [total_Ah],
  type: 'line'
};

var data7 = [trace7];
Plotly.plot('chartAhMin',data7, layout7);

setInterval(function(){
  Plotly.extendTraces('chartAhMin',{x:[[getTime()]], y:[[total_Ah]]}, [0]);
}, 1000);


// publish messages to the Raspberry Pi

//start race, and set the battery Ah and time.
startRace = function(){
    var battery_Total_Ah =  document.getElementById("battery_Total").value;
    var total_time_val =  document.getElementById("Total_time").value;
    var output_string = {'Battery': battery_Total_Ah, 'Time': total_time_val};
    
    submitUpdate('Houston', output_string);
}

//update the remaining time
updateTime = function(){
    var total_time_val =  document.getElementById("Total_time").value;
    var output_string = {'Time': total_time_val};
    
    submitUpdate('Houston', output_string);
}

//send the targe ah per min expendature
sendTarget = function(){
    var target_ah =  document.getElementById("Target_val").value;
    submitUpdate('Houston', {'Target': target_ah});
    //test 
    
      perdictDataAhIn(0, 10);
}

//set which prediction mode the Raspberry Pi is in.
autoModeSet =  function(){
    var perdiction_mode =  'auto';
    submitUpdate('Houston', {'Prediction Mode': perdiction_mode});
}

semiAutoModeSet =  function(){
    var perdiction_mode =  'semi-auto';
    submitUpdate('Houston', {'Prediction Mode': perdiction_mode});
}

manModeSet =  function(){
    var perdiction_mode =  'man';
    submitUpdate('Houston', {'Prediction Mode': perdiction_mode});
}

//send which signal for manual mode
sendSignalSlower =  function(){
    var send_signal_mode =  'Slow Down';
    submitUpdate('Houston', {'Speed Signal': send_signal_mode});
}

sendSignalOnspeed =  function(){
    var send_signal_mode =  'Center';
    submitUpdate('Houston', {'Speed Signal': send_signal_mode});
}

sendSignalFaster =  function(){
    var send_signal_mode =  'Speed Up';
    submitUpdate('Houston', {'Speed Signal': send_signal_mode});
}