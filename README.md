# 🥏 Discus Throw Simulator

A physics-based interactive simulation of a discus throw built with **Python and Pygame**.  
The project models projectile motion using real-world parameters and visualizes how angle, velocity, and initial height affect the trajectory of a thrown object.

---

## 🎯 Purpose of the Project

This simulator was created as a **mathematical and physics visualization tool** for studying projectile motion.

It demonstrates how the motion of a discus can be described using a parabolic trajectory derived from classical mechanics:

- Initial velocity (`v`)
- Launch angle (`θ`)
- Initial height (`h₀`)
- Gravity (`g`)

The goal is to make abstract physics concepts **interactive, visual, and intuitive**.

---

## 🧠 Mathematical Model

The projectile motion is based on the equation:

\[
y = x \tan(\theta) - \frac{g x^2}{2 v^2 \cos^2(\theta)}
\]

Where:
- \( \theta \) — launch angle (degrees)
- \( v \) — initial velocity (m/s)
- \( h₀ \) — initial height (m)
- \( g \) — gravitational acceleration

The simulation also allows real-time adjustment of:
- Launch angle (θ)
- Velocity (v)
- Starting height (h₀)

---

## 🖥️ Features

### 🎮 Interactive Controls
- Real-time sliders for:
  - Angle (θ in degrees)
  - Velocity (v in m/s)
  - Initial height (h₀ in cm)

### 📊 Live Visualization
- Stickman thrower representation
- Background stadium environment
- Real-time physics simulation

### 📐 Mathematical Display
- On-screen projectile motion equation
- Live parameter updates
- Unit-aware values (°, m/s, cm → m conversion)

### 🧩 Modular Architecture
- Separate UI components:
  - Slider system
  - Formula panel
  - Slider panel
- Physics logic separated from rendering

---

## 🧪 How It Works

1. The user adjusts sliders for:
   - θ (launch angle)
   - v (velocity)
   - h₀ (initial height)

2. The physics engine computes motion step-by-step using time integration.

3. The object is rendered frame-by-frame following a parabolic trajectory.

4. The formula panel updates in real-time to reflect current parameters.

---