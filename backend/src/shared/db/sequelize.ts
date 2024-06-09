import { Sequelize } from 'sequelize-typescript';
import path from 'path';

const sequelize = new Sequelize(process.env.DATABASE_URL as string, {
  dialect: 'postgres',  
  models: [path.join(__dirname, '../../modules/**/v1/*.model.ts')], 
  logging: false,  
  define: {
    freezeTableName: true,  
    timestamps: true         
  }
});

export default sequelize;
