import { Column, DataType, ForeignKey, Model, PrimaryKey, Table } from "sequelize-typescript";
import { User } from "../../../user/v1/models";
import { Plan } from "./Plan";

@Table({
    underscored: true,
    tableName: "subscriptions",
    modelName: "Subscription",
    timestamps: true  
})
export class Subscription extends Model {
    @PrimaryKey
    @Column({
        type: DataType.UUID,
        allowNull: false,
        defaultValue: DataType.UUIDV4 
    })
    id: string;

    @ForeignKey(() => User)
    @Column({
        type: DataType.UUID,
        allowNull: false
    })
    userId: string;

    @ForeignKey(() => Plan)
    @Column({
        type: DataType.INTEGER,
        allowNull: true 
    })
    planId: number;

    @Column({
        type: DataType.STRING,
        allowNull: true 
    })
    stripeSubscriptionId: string;

    @Column({
        type: DataType.DATE,
        allowNull: false 
    })
    startDate: Date;

    @Column({
        type: DataType.DATE,
        allowNull: false
    })
    endDate: Date;

    @Column({
        type: DataType.BOOLEAN,
        allowNull: false,
        defaultValue: false 
    })
    isTrial: boolean;

    @Column({
        type: DataType.ENUM,
        allowNull: false,
        values: ['active', 'cancelled', 'paused', 'past_due', 'trial'],
        defaultValue: 'trial' 
    })
    status: string;
}