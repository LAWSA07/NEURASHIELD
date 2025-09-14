import React, { useState, useEffect } from 'react';

const SimpleAlertsPage = () => {
  const [alerts, setAlerts] = useState([]);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState(null);
  const [lastMessage, setLastMessage] = useState(null);

  useEffect(() => {
    const connectWebSocket = () => {
      try {
        const ws = new WebSocket('ws://localhost:8001/ws');
        
        ws.onopen = () => {
          console.log('WebSocket connected');
          setIsConnected(true);
          setError(null);
        };
        
        ws.onmessage = (event) => {
          console.log('Received message:', event.data);
          setLastMessage(event.data);
          
          try {
            const data = JSON.parse(event.data);
            if (data.type === 'alert' && data.data) {
              setAlerts(prev => [data.data, ...prev]);
            } else if (data.type === 'initial' && data.alerts) {
              setAlerts(data.alerts);
            }
          } catch (err) {
            console.error('Error parsing message:', err);
          }
        };
        
        ws.onclose = () => {
          console.log('WebSocket disconnected');
          setIsConnected(false);
        };
        
        ws.onerror = (error) => {
          console.error('WebSocket error:', error);
          setError('WebSocket connection error');
          setIsConnected(false);
        };
        
        return ws;
      } catch (err) {
        console.error('Error creating WebSocket:', err);
        setError('Failed to create WebSocket connection');
        return null;
      }
    };

    const ws = connectWebSocket();
    
    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, []);

  const createTestAlert = async () => {
    try {
      const response = await fetch('http://localhost:8001/test-alert', {
        method: 'POST'
      });
      const data = await response.json();
      console.log('Test alert created:', data);
    } catch (err) {
      console.error('Error creating test alert:', err);
    }
  };

  const clearAlerts = () => {
    setAlerts([]);
  };

  return (
    <div className="container mx-auto px-4 py-6">
      <h1 className="text-2xl font-bold mb-4 text-white">Direct Alert Monitor</h1>
      
      <div className="bg-red-50 border-red-200 border p-4 rounded-lg mb-6">
        <h2 className="font-semibold text-red-700 mb-2">About This Page</h2>
        <p className="text-red-700 mb-2">
          This page uses a completely standalone approach to display alerts with minimal dependencies.
          The WebSocket connection is established directly in the component, bypassing all other services.
        </p>
        <p className="text-red-700">
          If you see alerts on this page but not elsewhere in the application, it indicates an issue with 
          the service implementation or state management in other components, not with the WebSocket or backend.
        </p>
      </div>
      
      {/* Connection Status */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-lg font-semibold mb-4">Connection Status</h2>
        <div className="flex items-center space-x-4 mb-4">
          <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
          <span className="font-medium">{isConnected ? 'Connected' : 'Disconnected'}</span>
        </div>
        
        <div className="flex space-x-3 mb-4">
          <button
            onClick={() => window.location.reload()}
            className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
          >
            Connect
          </button>
          <button
            onClick={() => window.location.reload()}
            className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700"
          >
            Disconnect
          </button>
          <button
            onClick={() => window.location.reload()}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
          >
            Reset
          </button>
        </div>
        
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}
      </div>
      
      {/* Test Controls */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-lg font-semibold mb-4">Test Controls</h2>
        <div className="flex space-x-3">
          <button
            onClick={createTestAlert}
            className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700"
          >
            + Create Test Alert
          </button>
          <button
            onClick={clearAlerts}
            className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700"
          >
            Clear Alerts
          </button>
        </div>
      </div>
      
      {/* Alerts Display */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold mb-4">Alerts ({alerts.length})</h2>
        {alerts.length === 0 ? (
          <div className="text-center py-8">
            <div className="text-yellow-500 text-4xl mb-2">⚠️</div>
            <p className="text-gray-600">No alerts received yet</p>
            <p className="text-sm text-gray-500 mt-2">
              Try creating a test alert or wait for real threats
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {alerts.map((alert, index) => (
              <div key={alert.id || index} className="border border-gray-200 rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-semibold text-lg">{alert.threat_type}</h3>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    alert.severity === 'high' ? 'bg-red-100 text-red-800' :
                    alert.severity === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-green-100 text-green-800'
                  }`}>
                    {alert.severity?.toUpperCase() || 'UNKNOWN'}
                  </span>
                </div>
                <p className="text-gray-600 mb-2">{alert.description}</p>
                <div className="text-sm text-gray-500">
                  <p>Method: {alert.detection_method}</p>
                  <p>Confidence: {(alert.confidence * 100).toFixed(1)}%</p>
                  <p>Time: {new Date(alert.timestamp).toLocaleTimeString()}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      
      <div className="mt-6 p-4 bg-gray-50 rounded-lg border">
        <h2 className="font-semibold mb-2">Troubleshooting Tips</h2>
        <div className="space-y-4">
          <div>
            <h3 className="font-medium">If no connection is established:</h3>
            <ul className="list-disc list-inside space-y-1 mt-1 ml-2">
              <li>Make sure the backend server is running at http://localhost:8000</li>
              <li>Check that the WebSocket endpoint is available at ws://localhost:8000/ws</li>
              <li>Use the "Reset Connection" button to force a reconnection attempt</li>
              <li>Look for CORS errors in your browser console</li>
            </ul>
          </div>
          
          <div>
            <h3 className="font-medium">If connected but no alerts appear:</h3>
            <ul className="list-disc list-inside space-y-1 mt-1 ml-2">
              <li>Use the "Create Test Alert" button to generate a test alert</li>
              <li>Check the "Last Raw Message" section to see if any data is being received</li>
              <li>Verify that the backend is properly generating and broadcasting alerts</li>
              <li>Check if there are any parse errors in your browser console</li>
              <li>Try the "Reset Connection" button to establish a fresh connection</li>
            </ul>
          </div>
          
          <div>
            <h3 className="font-medium">Backend Commands to Test:</h3>
            <div className="bg-gray-100 p-2 rounded font-mono text-sm mt-1 overflow-x-auto">
              <p className="mb-1">curl http://localhost:8000/test-alert</p>
              <p>curl http://localhost:8000/debug/alerts</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SimpleAlertsPage; 