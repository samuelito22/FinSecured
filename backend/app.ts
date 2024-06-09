import express, {Request, Response} from 'express';
import bodyParser from 'body-parser';
import morgan from 'morgan';
import UserRoutesV1 from "./src/modules/user/v1/routes"

const app = express();

// Middleware
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

if (process.env.NODE_ENV === 'development') {
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