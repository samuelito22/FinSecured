import { BelongsTo, Column, CreatedAt, DataType, ForeignKey, Model, PrimaryKey, Table } from "sequelize-typescript";
import { User } from "./User.model";

@Table({
    underscored: true,
    timestamps: false,
    tableName: 'feedbacks',
    modelName: 'Feedback'
})
export class Feedback extends Model {
    @PrimaryKey
    @Column({
        type: DataType.UUID,
        defaultValue: DataType.UUIDV4 ,
        allowNull: false
    })
    id: string

    @ForeignKey(() => User)
    @Column({
        type: DataType.UUID
    })
    userId: string;

    @Column({
        type: DataType.STRING,
        allowNull: false
    })
    content: string

    @CreatedAt
    createdAt: Date;

    @BelongsTo(() => User)
    user: User;
}