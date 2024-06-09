import { Model, Table } from "sequelize-typescript";

@Table({
    underscored: true,
    tableName: "plans",
    modelName: "Plan",
    timestamps: true  
})
export class Plan extends Model {
}