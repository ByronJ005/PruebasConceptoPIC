<template>
  <div class="landing-page">
    <!-- Header / Navbar -->
    <header class="navbar">
      <div class="logo">
        <span class="icon">🚌</span>
        <h1>Terminal Loja</h1>
      </div>
      <nav class="nav-links">
        <router-link to="/login" class="nav-btn btn-outline">Iniciar Sesión</router-link>
        <router-link to="/register" class="nav-btn btn-primary">Registrarse</router-link>
      </nav>
    </header>

    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <h2>Tus viajes desde Loja, a un clic de distancia</h2>
        <p>Reserva tus boletos de forma rápida, segura y elige tu asiento preferido. Trabajamos con las mejores cooperativas de transporte para llevarte a tu destino.</p>
        <div class="hero-cta">
          <router-link to="/register" class="btn btn-primary">Buscar Boletos</router-link>
          <router-link to="/login" class="btn btn-secondary">Ya tengo cuenta</router-link>
        </div>
      </div>
      <div class="hero-image">
        <img src="https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?q=80&w=800&auto=format&fit=crop" alt="Bus en la carretera" />
      </div>
    </section>

    <!-- Services / Benefits -->
    <section class="services">
      <h3>¿Por qué elegirnos?</h3>
      <div class="services-grid">
        <div class="service-card">
          <div class="service-icon">⚡</div>
          <h4>Compra Rápida</h4>
          <p>Adquiere tus pasajes en menos de 2 minutos, sin hacer filas.</p>
        </div>
        <div class="service-card">
          <div class="service-icon">💺</div>
          <h4>Elección de Asiento</h4>
          <p>Visualiza el bus y escoge tu asiento favorito al instante.</p>
        </div>
        <div class="service-card">
          <div class="service-icon">🤝</div>
          <h4>Múltiples Cooperativas</h4>
          <p>Compara horarios y precios entre varias cooperativas de Loja.</p>
        </div>
        <div class="service-card">
          <div class="service-icon">🔒</div>
          <h4>Seguridad Garantizada</h4>
          <p>Tus pagos y datos personales están protegidos con la más alta seguridad.</p>
        </div>
      </div>
    </section>

    <!-- Popular Destinations -->
    <section class="destinations">
      <h3>Destinos Populares desde Loja</h3>
      <div class="destinations-grid">
        <div class="destination-card">
          <img src="https://images.unsplash.com/photo-1590523277543-a94d2e4eb00b?q=80&w=400&auto=format&fit=crop" alt="Quito" />
          <div class="destination-info">
            <h4>Quito</h4>
          </div>
        </div>
        <div class="destination-card">
          <img src="https://images.unsplash.com/photo-1583217874534-581393fd5325?q=80&w=400&auto=format&fit=crop" alt="Guayaquil" />
          <div class="destination-info">
            <h4>Guayaquil</h4>
          </div>
        </div>
        <div class="destination-card">
          <img src="https://images.unsplash.com/photo-1518086055593-5d3c8c76eb9a?q=80&w=400&auto=format&fit=crop" alt="Cuenca" />
          <div class="destination-info">
            <h4>Cuenca</h4>
          </div>
        </div>
        <div class="destination-card">
          <img src="https://images.unsplash.com/photo-1614088824147-9f4a9b5a0342?q=80&w=400&auto=format&fit=crop" alt="Machala" />
          <div class="destination-info">
            <h4>Machala</h4>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-content">
        <div class="footer-brand">
          <h4>Terminal Terrestre de Loja</h4>
          <p>Conectando destinos, uniendo caminos.</p>
        </div>
        <div class="footer-links">
          <h4>Enlaces Rápidos</h4>
          <router-link to="/login">Iniciar Sesión</router-link>
          <router-link to="/register">Registrarse</router-link>
        </div>
        <div class="footer-contact">
          <h4>Contacto</h4>
          <p>📍 Av. 8 de Diciembre, Loja, Ecuador</p>
          <p>📞 (07) 257-XXXX</p>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; {{ new Date().getFullYear() }} Sistema de Reserva de Boletos - Loja. Todos los derechos reservados.</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
// Landing Page logic (currently static)
</script>

<style scoped>
.landing-page {
  font-family: 'Inter', sans-serif;
  color: #1f2937;
  background-color: #f9fafb;
}

/* Navbar */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 5%;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  position: sticky;
  top: 0;
  z-index: 100;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.logo h1 {
  font-size: 1.5rem;
  margin: 0;
  color: #0369a1; /* Loja Blue tone */
}

.nav-links {
  display: flex;
  gap: 1rem;
}

.nav-btn {
  text-decoration: none;
  padding: 0.5rem 1.25rem;
  border-radius: 6px;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-outline {
  border: 1px solid #0ea5e9;
  color: #0ea5e9;
}

.btn-outline:hover {
  background: #f0f9ff;
}

.btn-primary {
  background: #0ea5e9;
  color: white;
  border: 1px solid #0ea5e9;
}

.btn-primary:hover {
  background: #0284c7;
}

/* Hero Section */
.hero {
  display: flex;
  flex-direction: column-reverse;
  align-items: center;
  padding: 4rem 5%;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  gap: 2rem;
}

@media (min-width: 768px) {
  .hero {
    flex-direction: row;
    justify-content: space-between;
  }
}

.hero-content {
  flex: 1;
  max-width: 600px;
}

.hero-content h2 {
  font-size: 2.5rem;
  color: #0c4a6e;
  line-height: 1.2;
  margin-bottom: 1.5rem;
}

.hero-content p {
  font-size: 1.125rem;
  color: #475569;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.hero-cta {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn {
  text-decoration: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.2s;
  text-align: center;
}

.btn-secondary {
  background: #f1f5f9;
  color: #334155;
  border: 1px solid #cbd5e1;
}

.btn-secondary:hover {
  background: #e2e8f0;
}

.hero-image {
  flex: 1;
  display: flex;
  justify-content: center;
}

.hero-image img {
  max-width: 100%;
  border-radius: 12px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

/* Services */
.services {
  padding: 5rem 5%;
  text-align: center;
  background: white;
}

.services h3, .destinations h3 {
  font-size: 2rem;
  color: #0f172a;
  margin-bottom: 3rem;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.service-card {
  padding: 2rem;
  background: #f8fafc;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease;
}

.service-card:hover {
  transform: translateY(-5px);
}

.service-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.service-card h4 {
  font-size: 1.25rem;
  color: #1e293b;
  margin-bottom: 1rem;
}

.service-card p {
  color: #64748b;
  line-height: 1.5;
}

/* Destinations */
.destinations {
  padding: 5rem 5%;
  background: #f1f5f9;
  text-align: center;
}

.destinations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
}

.destination-card {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.destination-card img {
  width: 100%;
  height: 250px;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.destination-card:hover img {
  transform: scale(1.05);
}

.destination-info {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
  padding: 1.5rem 1rem 1rem;
  color: white;
  text-align: left;
}

.destination-info h4 {
  margin: 0;
  font-size: 1.25rem;
}

/* Footer */
.footer {
  background: #0f172a;
  color: #cbd5e1;
  padding: 4rem 5% 2rem;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 3rem;
  margin-bottom: 3rem;
}

.footer-brand h4 {
  color: white;
  font-size: 1.25rem;
  margin-bottom: 1rem;
}

.footer-links h4, .footer-contact h4 {
  color: white;
  margin-bottom: 1rem;
}

.footer-links a {
  display: block;
  color: #94a3b8;
  text-decoration: none;
  margin-bottom: 0.5rem;
  transition: color 0.2s;
}

.footer-links a:hover {
  color: white;
}

.footer-contact p {
  margin-bottom: 0.5rem;
}

.footer-bottom {
  text-align: center;
  padding-top: 2rem;
  border-top: 1px solid #334155;
  font-size: 0.875rem;
}
</style>
