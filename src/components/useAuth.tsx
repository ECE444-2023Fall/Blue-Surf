import { useState } from 'react';

interface User {
  userId: string;
  username: string;
}

function useAuth() {
  function getToken(): string | null {
    const userToken = localStorage.getItem('token');
    return userToken ? userToken : null;
  }

  function getUserInfo(): User | null {
    const userInfo = localStorage.getItem('user');
    return userInfo ? JSON.parse(userInfo) : null;
  }

  const [token, setToken] = useState<string | null>(getToken());
  const [user, setUser] = useState<User | null>(getUserInfo());

  function saveAuth(userToken: string, userInfo: User) {
    localStorage.setItem('token', userToken);
    localStorage.setItem('user', JSON.stringify(userInfo));
    setToken(userToken);
    setUser(userInfo);
  }

  function removeAuth() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setToken(null);
    setUser(null);
  }

  return {
    setAuth: saveAuth,
    token,
    user,
    removeAuth,
  };
}

export default useAuth;
