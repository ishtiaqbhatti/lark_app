import { useContext } from 'react';
import { ClientContext } from '../context/ClientContext';

// Simple wrapper hook to ensure useClient is used within its Provider
export const useClient = () => {
    const context = useContext(ClientContext);
    if (context === undefined) {
        throw new Error('useClient must be used within a ClientProvider');
    }
    return context;
};
