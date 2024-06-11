import express, {Request, Response} from 'express';
import bodyParser from 'body-parser';
import morgan from 'morgan';
import UserRoutesV1 from "./src/modules/user/v1/routes"
import { config } from './src/shared/config';

const app = express();

// Middleware
app.use((req, res, next) => {
  if (req.originalUrl === '/api/v1/subscriptions/stripe-webhook') {
    next();
  } else {
    bodyParser.json()(req, res, next);
  }
});

app.use(bodyParser.urlencoded({ extended: true }));

if (config.env === 'development') {
    app.use(morgan('dev'));
  }
  

const v1 = express.Router();

v1.use("/users", UserRoutesV1)

app.use('/api/v1', v1);

// Catch-all route for unhandled requests
app.use('*', (req, res) => {
    res.status(404).send('API endpoint is inexistent.');
  });

export default app