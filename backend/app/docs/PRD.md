# IronPath - Product Requirements Document

## Overview

IronPath is an intelligent gym progression platform that helps users achieve their strength and physique goals through personalized workout programming, adaptive progression, and data-driven coaching.

Unlike traditional workout trackers, IronPath does not simply record workouts. It analyzes performance, predicts progress, and recommends what the user should do next.

---

## Problem Statement

Most fitness applications focus on logging workouts.

Users still have to decide:

- When to increase weight
- Whether they are progressing
- Whether they are strong for their bodyweight
- If they should deload
- If their program is effective

IronPath solves these problems by acting as an intelligent strength coach.

---

## Target Audience

- Beginners
- Intermediate lifters
- Advanced lifters
- Powerlifters
- Bodybuilders
- Fitness enthusiasts

---

## MVP Features

### Authentication

- Register
- Login
- JWT Authentication

---

### User Profile

- Age
- Height
- Bodyweight
- Gender
- Training experience
- Goal
- Training days
- Equipment

---

### Program Generator

The user answers onboarding questions.

IronPath generates a personalized training program.

Users may edit the generated program.

---

### Workout Logging

Users record:

- Weight
- Repetitions
- Sets
- RPE (optional)

---

### Progress Dashboard

Display:

- Estimated 1RM
- Weekly volume
- Bodyweight
- Personal records
- Goal progress

---

### Progression Engine

IronPath automatically determines:

- Increase weight
- Increase repetitions
- Repeat workout
- Deload

based on previous performance.

---

### AI Coach

Explain recommendations in natural language.

Example:

"Increase your bench press to 72.5 kg because you successfully completed your target for the last three sessions."

---

## Long-Term Features

- Mobile App
- Smartwatch Integration
- Trainer Dashboard
- Nutrition Tracking
- AI Form Analysis
- Wearable Integration

---

## Technology Stack

Frontend

- React
- TypeScript
- Tailwind CSS

Backend

- FastAPI
- PostgreSQL
- SQLAlchemy

Authentication

- JWT

Deployment

- Docker
- AWS

---

## Vision

IronPath aims to become an intelligent strength coaching platform that combines structured programming, adaptive progression, and AI guidance to help athletes consistently improve their performance.