-- Create the app database
CREATE DATABASE app OWNER app_admin;

-- Switch to app database
\c app

-- Create app schema owned by admin
CREATE SCHEMA app AUTHORIZATION app_admin;