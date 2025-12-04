// Generates VAPI JSON from form
function generateVAPIConfig() {
  return {
    name: document.getElementById('name').value,
    model: {
      provider: "openai",
      model: "gpt-4",
      messages: [{
        role: "system",
        content: document.getElementById('prompt').value
      }]
    },
    voice: {
      provider: "11labs",
      voiceId: document.getElementById('voice').value
    },
    firstMessage: document.getElementById('firstMsg').value,
    serverUrl: document.getElementById('webhook').value
  };
}

// Send to VAPI API
async function createAssistant() {
  const config = generateVAPIConfig();
  
  const response = await fetch('https://api.vapi.ai/assistant', {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer ' + VAPI_KEY,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(config)
  });
  
  const assistant = await response.json();
  alert('Assistant created! ID: ' + assistant.id);
}