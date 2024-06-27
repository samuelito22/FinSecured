import { BelongsTo, Column, CreatedAt, DataType, ForeignKey, Model, PrimaryKey, Table } from "sequelize-typescript";
import { User } from "./User.model";
import { Optional } from "sequelize";

interface FeedbackAttributes {
    id: string;
    userId: string;
    content: string;
    createdAt?: Date;
}

type FeedbackCreationAttributes = Optional<FeedbackAttributes, 'createdAt' | 'id'>;

@Table({
    underscored: true,
    timestamps: false,
    tableName: 'feedbacks',
    modelName: 'Feedback'
})
export class Feedback extends Model<FeedbackAttributes, FeedbackCreationAttributes> {
    @PrimaryKey
    @Column({
        type: DataType.UUID,
        defaultValue: DataType.UUIDV4 ,
        allowNull: false
    })
    id!: string

    @ForeignKey(() => User)
    @Column({
        type: DataType.UUID
    })
    userId!: string;

    @Column({
        type: DataType.STRING,
        allowNull: false
    })
    content!: string

    @CreatedAt
    createdAt!: Date;

    @BelongsTo(() => User)
    user!: User;
}