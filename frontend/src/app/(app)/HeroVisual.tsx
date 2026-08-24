'use client';

export default function HeroVisual() {
  return (
    <div className="w-full h-full flex items-center justify-center relative">
      <svg viewBox="0 0 400 320" className="max-w-full h-auto w-80" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">
        <defs>
          <radialGradient id="g1" cx="30%" cy="20%" r="80%">
            <stop offset="0%" stopColor="#7c3aed" stopOpacity="0.9" />
            <stop offset="60%" stopColor="#06b6d4" stopOpacity="0.3" />
            <stop offset="100%" stopColor="#0b0f19" stopOpacity="0" />
          </radialGradient>
          <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="6" result="coloredBlur" />
            <feMerge>
              <feMergeNode in="coloredBlur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        <rect x="0" y="0" width="100%" height="100%" rx="20" fill="url(#g1)" opacity="0.03" />

        {/* central wireframe */}
        <g transform="translate(200,160)">
          <circle cx="0" cy="0" r="92" fill="none" stroke="#14213d" strokeWidth="1" />
          {[0,45,90,135,180,225,270,315].map((ang, i) => (
            <line key={i} x1="0" y1="0" x2={(92*Math.cos((ang*Math.PI)/180)).toString()} y2={(92*Math.sin((ang*Math.PI)/180)).toString()} stroke="#0b1220" strokeWidth="0.8" />
          ))}

          {/* nodes */}
          <g filter="url(#glow)">
            <circle cx="-48" cy="-16" r="6" fill="#7c3aed" />
            <circle cx="28" cy="-60" r="5" fill="#06b6d4" />
            <circle cx="56" cy="20" r="7" fill="#8b5cf6" />
            <circle cx="-8" cy="64" r="5" fill="#06b6d4" />
            <circle cx="44" cy="-2" r="4" fill="#60a5fa" />
          </g>

          {/* connecting lines */}
          <path d="M-48,-16 L28,-60" stroke="#2a3a57" strokeWidth="1" />
          <path d="M-48,-16 L56,20" stroke="#2a3a57" strokeWidth="1" />
          <path d="M28,-60 L56,20" stroke="#2a3a57" strokeWidth="1" />
          <path d="M56,20 L-8,64" stroke="#2a3a57" strokeWidth="1" />
        </g>
      </svg>
    </div>
  );
}
