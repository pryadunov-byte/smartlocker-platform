"use client";

import dynamic from "next/dynamic";
import { useEffect, useState } from "react";

const Map = dynamic(() => import("react-map-gl").then((mod) => mod.default), { ssr: false });
const Marker = dynamic(() => import("react-map-gl").then((mod) => mod.Marker), { ssr: false });

interface MapWidgetProps {
  markers: { lat: number; lon: number; status: "online" | "offline" | "alert" }[];
}

export function MapWidget({ markers }: MapWidgetProps) {
  const [viewport, setViewport] = useState({ latitude: 55.751244, longitude: 37.618423, zoom: 4 });

  useEffect(() => {
    if (markers.length) {
      setViewport((prev) => ({ ...prev, latitude: markers[0].lat, longitude: markers[0].lon, zoom: 9 }));
    }
  }, [markers]);

  return (
    <div className="card h-[420px]">
      <h2 className="text-lg font-semibold mb-4">Карта устройств</h2>
      <Map
        {...viewport}
        mapStyle="https://demotiles.maplibre.org/style.json"
        onMove={(evt) => setViewport(evt.viewState as typeof viewport)}
        style={{ width: "100%", height: "320px" }}
      >
        {markers.map((marker, idx) => (
          <Marker key={idx} latitude={marker.lat} longitude={marker.lon}>
            <div
              style={{
                backgroundColor:
                  marker.status === "online" ? "#22c55e" : marker.status === "alert" ? "#f97316" : "#ef4444",
                width: 14,
                height: 14,
                borderRadius: "50%",
                border: "2px solid white"
              }}
            />
          </Marker>
        ))}
      </Map>
    </div>
  );
}
