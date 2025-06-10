import { useState, useCallback } from 'react';
import { createApiRequest } from '../config/api';

export const useApi = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);

  const execute = useCallback(async (endpoint, options = {}) => {
    try {
      setLoading(true);
      setError(null);
      const result = await createApiRequest(endpoint, options);
      setData(result);
      return result;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    loading,
    error,
    data,
    execute,
  };
}; 