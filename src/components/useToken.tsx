import { useState } from 'react';

function useToken() {
  function getToken(): string | null {
    const userToken = localStorage.getItem('token');
    return userToken ? userToken : null;
  }

  const [token, setToken] = useState<string | null>(getToken());

  function saveToken(userToken: string) {
    localStorage.setItem('token', userToken);
    setToken(userToken);
  }

  function removeToken() {
    localStorage.removeItem('token');
    setToken(null);
  }

  return {
    setToken: saveToken,
    token,
    removeToken,
  };
}

export default useToken;
