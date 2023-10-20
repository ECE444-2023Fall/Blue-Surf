-- User Table
CREATE TABLE User (
  user_id SERIAL PRIMARY KEY,
  username VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  user_profile_created BOOLEAN NOT NULL
);

-- Event Table
CREATE TABLE Event (
  event_id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  location VARCHAR(255),
  start_time TIMESTAMP NOT NULL,
  end_time TIMESTAMP NOT NULL,
  user_id INT REFERENCES User(user_id),
  is_published BOOLEAN NOT NULL,
  is_public BOOLEAN NOT NULL,
  like_count INT
);

-- Club Table
CREATE TABLE Club (
  club_id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  leader_id INT REFERENCES User(user_id),
  membership_count INT
);

-- EventAttendee Table
CREATE TABLE EventAttendee (
  event_attendee_id SERIAL PRIMARY KEY,
  event_id INT REFERENCES Event(event_id),
  user_id INT REFERENCES User(user_id)
);

-- UserClubMembership Table
CREATE TABLE UserClubMembership (
  user_club_membership_id SERIAL PRIMARY KEY,
  user_id INT REFERENCES User(user_id),
  club_id INT REFERENCES Club(club_id),
  join_date DATE NOT NULL,
  is_subscribed BOOLEAN NOT NULL
);

-- UserInterestedEvent Table
CREATE TABLE UserInterestedEvent (
  user_interested_event_id SERIAL PRIMARY KEY,
  user_id INT REFERENCES User(user_id),
  event_id INT REFERENCES Event(event_id)
);

-- AdministratorDashboardMetrics Table
CREATE TABLE AdministratorDashboardMetrics (
  metrics_id SERIAL PRIMARY KEY,
  event_id INT REFERENCES Event(event_id),
  interest_count INT,
);

-- User Profile Table
CREATE TABLE UserProfile (
  profile_id SERIAL PRIMARY KEY,
  user_id INT REFERENCES User(user_id),
  profile_data JSON -- You can specify the actual JSON structure
);
