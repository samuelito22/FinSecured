import { Optional } from "sequelize";
import { AutoIncrement, Column, DataType, Index, Model, PrimaryKey, Table } from "sequelize-typescript";

interface PlanAttributes {
    id: number;
    stripePlanId: string;
    stripePriceId: string;
    name: string;
    price: number;
    interval: 'monthly' | 'yearly';
    description?: string;
    createdAt?: Date;
    updatedAt?: Date;
}

type PlanCreationAttributes = Optional<PlanAttributes, 'description' | 'createdAt' | 'updatedAt' | 'id'>;

@Table({
    underscored: true,
    tableName: "plans",
    modelName: "Plan",
    timestamps: true  
})
export class Plan extends Model<PlanAttributes, PlanCreationAttributes> {
    @PrimaryKey
    @AutoIncrement
    @Column({
        type: DataType.INTEGER,
    })
    id!: number;

    @Index
    @Column({
        type: DataType.STRING,
        allowNull: false,
    })
    stripePlanId!: string;

    @Index
    @Column({
        type: DataType.STRING,
        allowNull: false,
        unique: true,
    })
    stripePriceId!: string;

    @Column({
        type: DataType.STRING,
        allowNull: false
    })
    name!: string;

    @Column({
        type: DataType.TEXT
    })
    description?: string;

    @Column({
        type: DataType.DECIMAL(10, 2),
        allowNull: false
    })
    price!: number;

    @Column({
        type: DataType.ENUM,
        values: ['monthly', 'yearly']
    })
    interval!: 'monthly' | 'yearly';
}
