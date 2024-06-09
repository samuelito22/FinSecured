import { Column, CreatedAt, DataType, HasOne, Model, Table, UpdatedAt } from "sequelize-typescript";
import { UserProfile } from "./UserProfile.model";

@Table({
    timestamps: true,
    tableName:"users",
    modelName:"User",
    underscored: true
})
export class User extends Model {
    @Column({
        primaryKey: true,
        type: DataType.UUID,
        allowNull: false
    })
    id: string;

    @CreatedAt
    createdAt: Date;

    @UpdatedAt
    updatedAt: Date;

    @HasOne(() => UserProfile)
    userProfile: UserProfile;
}