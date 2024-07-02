import express from 'express';
import bodyParser from 'body-parser';
import morgan from 'morgan';
import UserRoutesV1 from "./modules/user/v1/routes"
import DocumentRoutesV1 from "./modules/document/v1/routes"
import { config } from './shared/config';
import cors from "cors"

const app = express();

app.use(cors({
  origin: ['http://localhost:3000'],
  credentials: true 
}));

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
v1.use("/documents", DocumentRoutesV1)

app.use('/api/v1', v1);

// Catch-all route for unhandled requests
app.use('*', (req, res) => {
    res.status(404).send('API endpoint is inexistent.');
  });

export default app