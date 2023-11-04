import React, { useState } from 'react';
import Login from './LoginPage';
import LoginPage from './LoginPage';

const LandingPage: React.FC = () => {
  const [token, setToken] = useState<string | undefined>(undefined);

  if (!token) {
    return <Login setToken={setToken} />;
  }

  return (
    <div className='text-white font-bold text-2xl'>Dashboard</div>
  );
};

export default LoginPage;