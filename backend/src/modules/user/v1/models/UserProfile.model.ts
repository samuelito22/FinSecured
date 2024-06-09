import { BelongsTo, Column, CreatedAt, DataType, ForeignKey, Model, PrimaryKey, Table, UpdatedAt } from "sequelize-typescript";
import { User } from "./User.model";

@Table({
    timestamps: true,
    tableName:"user_profiles",
    modelName:"UserProfile",
    underscored: true
})
export class UserProfile extends Model {
    @PrimaryKey
    @ForeignKey(() => User)
    @Column({
        type: DataType.UUID
    })
    userId: string;

    @Column({
        type: DataType.STRING(255),
        unique: true,
        allowNull: false
    })
    email: string;

    @Column({
        type: DataType.STRING(50),
        allowNull: true
    })
    phoneNumber: string;

    @Column({
        type: DataType.STRING(255),
        allowNull: true
    })
    organization: string;

    @CreatedAt
    createdAt: Date;

    @UpdatedAt
    updatedAt: Date;

    @BelongsTo(() => User)
    user: User;
}