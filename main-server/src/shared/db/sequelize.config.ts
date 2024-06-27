import { Sequelize } from 'sequelize-typescript';
import path from 'path';
import { config } from '../config';

const sequelize = new Sequelize(config.database.mainDatabaseUrl, {
  dialect: 'postgres',  
  models: [path.join(__dirname, '../../modules/**/v1/*.model.ts')], 
  logging: false,  
  define: {
    freezeTableName: true,  
    timestamps: true         
  }
});

export default sequelize;
