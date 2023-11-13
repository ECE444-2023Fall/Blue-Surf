import React, { useState } from 'react';
import axios, { AxiosResponse } from 'axios';

interface User {
  userId: string;
  username: string;
}

interface ProfileProps {
  token: string;
  user: User;
  setAuth: (token: string | null, user: User | null) => void;
}

const Profile: React.FC<ProfileProps> = (props) => {
  const [profileData, setProfileData] = useState<{ profile_name: string; about_me: string } | null>(null);

  const getData = () => {
    axios({
      method: 'GET',
      url:`${API_URL}/api/profile`,
      headers: {
        Authorization: 'Bearer ' + props.token,
      },
    })
      .then((response: AxiosResponse<any>) => {
        const res = response.data;
        res.access_token && props.setAuth(res.access_token, props.user);
        setProfileData({
          profile_name: res.name,
          about_me: res.about,
        });
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
          console.log(error.response.status);
          console.log(error.response.headers);
        }
      });
  };

  return (
    <div className="Profile">
      <p>To get your profile details: </p>
      <button onClick={getData}>Click me</button>
      {profileData && (
        <div>
          <p>Profile name: {profileData.profile_name}</p>
          <p>About me: {profileData.about_me}</p>
        </div>
      )}
    </div>
  );
};

export default Profile;
