from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    favorites: Mapped[List["Favorites"]] = relationship(
        "Favorites", back_populates="user", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "favorites": [favorite.serialize() for favorite in self.favorites],
        }

    """ def all_user_favorites(self):
        # print(self.favorites)
        results_favorites = list(map(lambda item: item.serialize(), self.favorites))
        return{
            "id": self.id,
            "username": self.username,
        } """
        
    def get_all_users(self):
        return {
            "user_id": self.id,
            "user_name": self.username
        }


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    homeworld_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))

    favorites: Mapped[List["Favorites"]] = relationship(
        back_populates="character")
    planet: Mapped["Planet"] = relationship(back_populates="characters")
    vehicles: Mapped[List["Vehicle"]] = relationship(
        back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "homeworld_id": self.homeworld_id
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    size: Mapped[int] = mapped_column(nullable=False)
    biome_type: Mapped[str] = mapped_column(String(120), nullable=False)

    favorites: Mapped[List["Favorites"]] = relationship(
        back_populates="planet")
    characters: Mapped[List["Character"]] = relationship(
        back_populates="planet")
    vehicles: Mapped[List["Vehicle"]] = relationship(back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "size": self.size,
            "biome_type": self.biome_type
        }


class Vehicle(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    manufacturing_planet_id: Mapped[int] = mapped_column(
        ForeignKey("planet.id"))
    character_owner_id: Mapped[int] = mapped_column(ForeignKey("character.id"))

    favorites: Mapped[List["Favorites"]] = relationship(
        back_populates="vehicle")
    planet: Mapped["Planet"] = relationship(back_populates="vehicles")
    character: Mapped["Character"] = relationship(back_populates="vehicles")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "manufacturing_planet_id": self.manufacturing_planet_id,
            "character_owner_id": self.character_owner_id
        }


class Favorites(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"), nullable=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicle.id"), nullable=True)

    user: Mapped["User"] = relationship(back_populates="favorites")
    character: Mapped["Character"] = relationship(back_populates="favorites")
    planet: Mapped["Planet"] = relationship(back_populates="favorites")
    vehicle: Mapped["Vehicle"] = relationship(back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
            "vehicle_id": self.vehicle_id
        }
