import { Table, Column, Model, DataType, PrimaryKey, CreatedAt, UpdatedAt, ForeignKey, BelongsTo, Index } from 'sequelize-typescript';
import { Optional } from 'sequelize';
import { User } from './User.model';

interface UserProfileAttributes {
    id: string;
    userId: string;
    organization: string;
    createdAt?: Date;
    updatedAt?: Date;
}

type UserProfileCreationAttributes = Optional<UserProfileAttributes, 'createdAt' | 'updatedAt' | 'id'>;

@Table({
    tableName: "user_profiles",
    timestamps: true,
    underscored: true
})
export class UserProfile extends Model<UserProfileAttributes, UserProfileCreationAttributes> {
    @PrimaryKey
    @Column({
        type: DataType.UUID,
        defaultValue: DataType.UUIDV4,
        allowNull: false
    })
    id!: string;

    @ForeignKey(() => User)
    @Index
    @Column({
        type: DataType.UUID
    })
    userId!: string;  // Definitely assigned in the application logic

    @Column({
        type: DataType.STRING(255),
        allowNull: false
    })
    organization!: string;  // Definitely assigned

    @CreatedAt
    createdAt!: Date;  // Managed by Sequelize, so we're sure it's initialized

    @UpdatedAt
    updatedAt!: Date;  // Managed by Sequelize, so we're sure it's initialized

    @BelongsTo(() => User)
    user?: User;  // Optional, as a user profile might not always have an associated user loaded
}
