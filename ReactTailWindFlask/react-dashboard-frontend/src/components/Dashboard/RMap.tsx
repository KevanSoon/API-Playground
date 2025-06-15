"use client";
import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { DivIcon } from "leaflet";

const singaporeCenter: [number, number] = [1.3521, 103.8198];

interface StationFeature {
  type: "Feature";
  geometry: {
    type: "Point";
    coordinates: [number, number];
  };
  properties: {
    name: string;
    stationId: string;
    rainfall_mm: number;
  };
}

interface GeoJSONResponse {
  type: "FeatureCollection";
  features: StationFeature[];
}

const RainfallMap: React.FC = () => {
  const [geoData, setGeoData] = useState<GeoJSONResponse | null>(null);

  const roundedRainyIcon = new DivIcon({
  html: `<img 
           src="https://cdn-icons-png.flaticon.com/512/414/414927.png" 
           style="border-radius: 50%; width: 30px; height: 30px;" 
         />`,
  className: "", // removes default leaflet styles on the div
  iconSize: [30, 30],
  iconAnchor: [15, 15],
  popupAnchor: [1, -34],
    });
  const roundedSunnyIcon = new DivIcon({
    html: `<img src="https://cdn-icons-png.flaticon.com/512/869/869869.png" style="border-radius:50%; width:30px; height:30px;" />`,
    className: "",
    iconSize: [30, 30],
    iconAnchor: [15, 15],
    popupAnchor: [1, -34],
    });


  useEffect(() => {
    fetch("http://127.0.0.1:5000/rainfallstations")
      .then((res) => res.json())
      .then((data: GeoJSONResponse) => setGeoData(data))
      .catch((err) => console.error("Error fetching rainfall data:", err));
  }, []);

  return (
    <MapContainer center={singaporeCenter} zoom={12} style={{ height: "100%", width: "100%" }}>
        <TileLayer url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png" />

      {geoData?.features.map((feature, idx) => (
        <Marker
          key={idx}
          position={[
            feature.geometry.coordinates[1],
            feature.geometry.coordinates[0]
          ]}
          icon={feature.properties.rainfall_mm > 0 ? roundedRainyIcon : roundedSunnyIcon}
        >
          <Popup>
            <strong>{feature.properties.name}</strong><br />
            Rainfall: {feature.properties.rainfall_mm} mm
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
};

export default RainfallMap;
