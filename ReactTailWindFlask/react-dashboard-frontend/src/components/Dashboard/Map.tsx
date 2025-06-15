"use client";
import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const singaporeCenter: [number, number] = [1.3521, 103.8198];

const MapWithGeoJSON: React.FC = () => {
  const [geoData, setGeoData] = useState<any>(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/denguecluster")
      .then((res) => res.json())
      .then((data) => setGeoData(data))
      .catch((err) => console.error("Failed to fetch GeoJSON:", err));
  }, []);

  return (
    <MapContainer center={singaporeCenter} zoom={12} style={{ height: "100%", width: "100%" }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {geoData && <GeoJSON data={geoData} />}
    </MapContainer>
  );
};

export default MapWithGeoJSON;
