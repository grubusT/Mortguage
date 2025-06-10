import { useState, useCallback } from 'react';
import { createApiRequest } from '../lib/api';

export const useApi = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);

  const execute = useCallback(async (endpoint: string, options: RequestInit = {}) => {
    try {
      setLoading(true);
      setError(null);
      const result = await createApiRequest(endpoint, options);
      setData(result);
      return result;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An error occurred';
      setError(errorMessage);
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