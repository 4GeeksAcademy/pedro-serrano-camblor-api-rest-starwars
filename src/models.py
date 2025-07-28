from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
""" from __future__ import annotations """
from typing import List

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favorites: Mapped[List["Favorites"]] = relationship(
        back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorites": self.favorites,
            # do not serialize the password, its a security breach
        }


class Favorites(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"))
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicle.id"))

    user: Mapped["User"] = relationship(back_populates="favorites")
    characters: Mapped["Character"] = relationship(back_populates="favorites")
    planets: Mapped["Planet"] = relationship(back_populates="favorites")
    vehicles: Mapped["Vehicle"] = relationship(back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id
        }


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    homeworld_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))

    favorites: Mapped[List["Favorites"]] = relationship(
        back_populates="character")
    planet: Mapped["Planet"] = relationship(
        back_populates="character")
    vehicle: Mapped["Vehicle"] = relationship(
        back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "homeworld_id": self.homeworld_id
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    size: Mapped[str] = mapped_column(
        String(120), unique=False, nullable=False)

    favorites: Mapped[List["Favorites"]] = relationship(
        back_populates="planet")
    characters: Mapped["Character"] = relationship(back_populates="planet")
    vehicles: Mapped["Vehicle"] = relationship(back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.email,
            "size": self.size
        }


class Vehicle(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    manufactoring_planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))
    character_owner_id: Mapped[int] = mapped_column(ForeignKey("character.id"))

    favorites: Mapped[List["Favorites"]] = relationship(
        back_populates="vehicle")
    planet: Mapped["Planet"] = relationship(
        back_populates="vehicle")
    character: Mapped["Character"] = relationship(
        back_populates="vehicle")


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "homeworld_id": self.homeworld_id
        }
