import app from './src/app';
import { config } from './src/shared/config';
import sequelize from './src/shared/db/sequelize.config';

const PORT = config.port || 3000;

let server: ReturnType<typeof app.listen> | undefined;

sequelize.authenticate() // First, confirm that the connection is successful
  .then(() => {
    console.log('Database connection has been established successfully. ');
    return sequelize.sync({ force: false, alter: true });  // Then synchronize models
  })
  .then(() => {
    console.log('Database connected and models synchronized. 🐘');
    server = app.listen(PORT, () => {
        console.log(`Server is up and running. Listening to port ${PORT}. 🐍`);
    });
  })
  .catch((error: Error) => {
    console.error('Failed to connect to the database or sync models:', error);
  });

const exitHandler = () => {
  if (server) {
    server.close(async () => {
      //logger.info('Server closed');
      await sequelize.close()
      process.exit(1);
    });
  } else {
    process.exit(1);
  }
};

const unexpectedErrorHandler = (error: Error) => {
  //logger.error(error);
  console.log(error)
  exitHandler();
};

process.on('uncaughtException', unexpectedErrorHandler);
process.on('unhandledRejection', unexpectedErrorHandler);

process.on('SIGTERM', () => {
  //logger.info('SIGTERM received');
  if (server) {
    server.close();
  }
});
