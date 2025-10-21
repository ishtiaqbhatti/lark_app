import React, { createContext, useContext, useState, useEffect } from 'react';

export const ClientContext = createContext();

export const useClient = () => useContext(ClientContext);

export const ClientProvider = ({ children }) => {
    const [clientId, setClientIdState] = useState(() => { // Renamed local state setter
        try {
            const storedClientId = localStorage.getItem('clientId'); // Changed key from 'currentClientId'
            return storedClientId ? storedClientId : 'Lark_Main_Site'; // Use a consistent default if not found
        } catch (error) {
            console.error("Could not access localStorage for clientId:", error);
            return 'Lark_Main_Site';
        }
    });

    useEffect(() => {
        try {
            localStorage.setItem('clientId', clientId); // Changed key from 'currentClientId'
        } catch (error) {
            console.error("Could not write to localStorage for clientId:", error);
        }
    }, [clientId]);
      
    // New function to update clientId and persist to localStorage
    const updateClientId = (newClientId) => {
        setClientIdState(newClientId);
        try {
            localStorage.setItem('clientId', newClientId); // Changed key from 'currentClientId'
        } catch (error) {
            console.error("Could not write to localStorage for clientId:", error);
        }
    };

    const value = { clientId, setClientId: updateClientId }; // Provide the wrapped setter

    return (
        <ClientContext.Provider value={value}>
            {children}
        </ClientContext.Provider>
    );
};