import dotenv from 'dotenv';
dotenv.config();

import app from './app';
import sequelize from './src/shared/db/sequelize';

const PORT = process.env.PORT || 3000;

sequelize.authenticate() // First, confirm that the connection is successful
  .then(() => {
    console.log('Database connection has been established successfully. ');
    return sequelize.sync({ force: false, alter: true });  // Then synchronize models
  })
  .then(() => {
    console.log('Database connected and models synchronized. 🐘');
    app.listen(PORT, () => {
        console.log(`Server is up and running. Listening to port ${PORT}. 🐍`);
    });
  })
  .catch((error: Error) => {
    console.error('Failed to connect to the database or sync models:', error);
  });
