import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";

// ------------------------------
// Inline SVG Icons (local, no CDN)
// ------------------------------
const TractorIcon = ({ className = "w-10 h-10", strokeWidth = 2 }) => (
  <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg" className={className} stroke="currentColor" strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round">
    <rect x="20" y="24" width="18" height="14" rx="2" />
    <rect x="12" y="20" width="10" height="10" rx="2" />
    <line x1="28" y1="20" x2="28" y2="14" />
    <circle cx="28" cy="12" r="1" fill="currentColor" />
    <line x1="38" y1="31" x2="48" y2="31" />
    <circle cx="18" cy="44" r="6" />
    <circle cx="42" cy="44" r="10" />
    <circle cx="18" cy="44" r="2" />
    <circle cx="42" cy="44" r="3" />
    <line x1="6" y1="54" x2="58" y2="54" />
  </svg>
);

const DeadLeafIcon = ({ className = "w-10 h-10", strokeWidth = 2 }) => (
  <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg" className={className} stroke="currentColor" strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round">
    <path d="M50 10C36 12 24 18 16 28s-12 24-4 26 18-6 26-14 14-20 12-30Z" />
    <path d="M12 52c8-2 18-10 26-18" />
    <path d="M30 26l-4 6" />
    <path d="M38 22l-3 4" />
    <path d="M24 36l-2 3" />
  </svg>
);

// ------------------------------
// Minimal UI primitives
// ------------------------------
const Button = ({ children, className = "", ...props }) => (
  <button className={"rounded-2xl px-4 py-2 font-semibold shadow-sm bg-indigo-600 text-white hover:bg-indigo-700 active:scale-[.98] transition " + className} {...props}>
    {children}
  </button>
);

const Card = ({ children, className = "" }) => (
  <div className={`rounded-3xl bg-white/90 backdrop-blur shadow-lg p-6 ${className}`}>{children}</div>
);

// ------------------------------
// Tiny Router (no external libs)
// ------------------------------
const Routes = {
  DASH: "DASH",
  DESIGN: "DESIGN",
  CARE: "CARE",
  DISEASE: "DISEASE",
};

function useRouter(initialRoute) {
  const [route, setRoute] = useState(() => sessionStorage.getItem("rb_route") || initialRoute);
  useEffect(() => sessionStorage.setItem("rb_route", route), [route]);
  return { route, navigate: setRoute };
}

// ------------------------------
// Local storage for design app URL
// ------------------------------
const LS_DESIGN_URL = "rb_design_url"; // string

// ------------------------------
// Screens (Dashboard + 3 features)
// ------------------------------
function Dashboard({ navigate }) {
  const [designURL, setDesignURL] = useState(() => localStorage.getItem(LS_DESIGN_URL) || "http://localhost:5000");

  const saveURL = () => {
    localStorage.setItem(LS_DESIGN_URL, designURL);
    alert("Design app URL saved.");
  };

  return (
    <div className="min-h-[100dvh] bg-gradient-to-br from-emerald-50 to-indigo-50 p-6">
      <div className="mx-auto max-w-6xl">
        <div className="flex items-center justify-between">
          <h2 className="text-3xl md:text-4xl font-extrabold text-slate-800">Roofbot</h2>
          <div className="flex items-center gap-2">
            <input className="w-64 rounded-2xl border px-3 py-2" value={designURL} onChange={(e) => setDesignURL(e.target.value)} title="Set your existing Garden Design app URL" />
            <Button className="bg-slate-700 hover:bg-slate-800" onClick={saveURL}>Save URL</Button>
          </div>
        </div>

        <p className="mt-2 text-slate-600">Choose what you want to do today.</p>

        <div className="grid md:grid-cols-3 gap-6 mt-8">
          <FeatureCard title="বাগান ডিজাইন" desc="আপনার বিদ্যমান প্রজেক্ট (ZIP) / Flask অ্যাপ লিঙ্ক করুন বা চালু করুন।" onClick={() => navigate(Routes.DESIGN)} icon={<TractorIcon className="w-10 h-10 text-emerald-600" />} />
          <FeatureCard title="কেয়ার প্ল্যান" desc="গাছের পানি, সার, সূর্য—সপ্তাহভিত্তিক পরিকল্পনা।" onClick={() => navigate(Routes.CARE)} icon={<span className="text-3xl">🗓️</span>} />
          <FeatureCard title="ডিজিজ চেক" desc="লিফ ইমেজ আপলোড করে রোগ নির্ণয় (ডেমো)." onClick={() => navigate(Routes.DISEASE)} icon={<DeadLeafIcon className="w-10 h-10 text-rose-600" />} />
        </div>
      </div>
    </div>
  );
}

const FeatureCard = ({ title, desc, onClick, icon }) => (
  <motion.button whileHover={{ y: -4 }} whileTap={{ scale: 0.98 }} onClick={onClick} className="text-left rounded-3xl bg-white shadow-lg p-6 hover:shadow-xl transition w-full">
    <div className="text-4xl">{icon}</div>
    <div className="mt-3 text-xl font-bold">{title}</div>
    <div className="text-slate-600 mt-1">{desc}</div>
  </motion.button>
);

function DesignEmbed({ navigate }) {
  const [url, setUrl] = useState(() => localStorage.getItem(LS_DESIGN_URL) || "http://localhost:5000");
  return (
    <div className="min-h-[100dvh] bg-slate-50 p-6">
      <div className="mx-auto max-w-6xl space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-2xl font-bold">Garden Design</h3>
          <Button className="bg-slate-700 hover:bg-slate-800" onClick={() => navigate(Routes.DASH)}>Back</Button>
        </div>
        <Card>
          <p className="text-slate-700">This page tries to embed your existing Flask app (from your ZIP project). If embedding is blocked by CORS or X-Frame-Options, use the “Open externally” button.</p>
          <div className="flex items-center gap-2 mt-3">
            <input className="w-80 rounded-2xl border px-3 py-2" value={url} onChange={(e) => setUrl(e.target.value)} />
            <a className="rounded-2xl px-4 py-2 font-semibold bg-emerald-600 text-white hover:bg-emerald-700" href={url} target="_blank">Open externally</a>
          </div>
        </Card>
        <div className="h-[70vh] rounded-2xl overflow-hidden shadow-lg border">
          <iframe src={url} title="Design App" className="w-full h-full bg-white" />
        </div>
      </div>
    </div>
  );
}

function CarePlan({ navigate }) {
  const [plant, setPlant] = useState("");
  const [sun, setSun] = useState("partial");
  const [season, setSeason] = useState("monsoon");
  const [plan, setPlan] = useState(null);

  const makePlan = () => {
    const baseline = {
      summer: { water: "Every day, morning", fert: "NPK 10-10-10, fortnightly", note: "Mulch to reduce evaporation" },
      monsoon: { water: "2–3×/week (rain dependent)", fert: "Every 3 weeks", note: "Check drainage" },
      winter: { water: "1–2×/week", fert: "Monthly", note: "Avoid overwatering" },
    };
    const b = baseline[season] || baseline.monsoon;
    const sAdj = sun === "full" ? "+ more water" : sun === "shade" ? "- less water" : "balanced";
    setPlan({ ...b, plant, sun, season, tip: sAdj });
  };

  return (
    <div className="min-h-[100dvh] bg-gradient-to-br from-emerald-50 to-indigo-50 p-6">
      <div className="mx-auto max-w-5xl space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-2xl font-bold">Care Plan</h3>
          <Button className="bg-slate-700 hover:bg-slate-800" onClick={() => navigate(Routes.DASH)}>Back</Button>
        </div>
        <Card>
          <div className="grid md:grid-cols-3 gap-4">
            <label className="block space-y-1 w-full">
              <span className="text-sm font-medium text-slate-700">Plant name</span>
              <input className="w-full rounded-2xl border px-4 py-2" value={plant} onChange={(e) => setPlant(e.target.value)} />
            </label>
            <label className="block">
              <span className="text-sm font-medium text-slate-700">Sun</span>
              <select className="w-full rounded-2xl border px-4 py-2" value={sun} onChange={(e) => setSun(e.target.value)}>
                <option value="full">Full sun</option>
                <option value="partial">Partial</option>
                <option value="shade">Shade</option>
              </select>
            </label>
            <label className="block">
              <span className="text-sm font-medium text-slate-700">Season</span>
              <select className="w-full rounded-2xl border px-4 py-2" value={season} onChange={(e) => setSeason(e.target.value)}>
                <option value="summer">Summer</option>
                <option value="monsoon">Monsoon</option>
                <option value="winter">Winter</option>
              </select>
            </label>
          </div>
          <div className="mt-4">
            <Button onClick={makePlan}>Generate plan</Button>
          </div>
        </Card>

        {plan && (
          <Card>
            <h4 className="text-xl font-bold">Weekly plan for {plan.plant || "your plant"}</h4>
            <ul className="list-disc pl-6 mt-2 space-y-1 text-slate-700">
              <li><b>Watering:</b> {plan.water} ({plan.tip})</li>
              <li><b>Fertilizer:</b> {plan.fert}</li>
              <li><b>Notes:</b> {plan.note}</li>
              <li><b>Sun exposure:</b> {plan.sun}</li>
              <li><b>Season:</b> {plan.season}</li>
            </ul>
          </Card>
        )}
      </div>
    </div>
  );
}

function DiseaseCheck({ navigate }) {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleUpload = (e) => {
    const f = e.target.files?.[0];
    if (!f) return;
    setFile(f);
    setTimeout(() => {
      const probs = [
        { label: "Leaf spot", score: Math.random().toFixed(2) },
        { label: "Rust", score: Math.random().toFixed(2) },
        { label: "Healthy", score: Math.random().toFixed(2) },
      ].sort((a, b) => Number(b.score) - Number(a.score));
      setResult(probs);
    }, 500);
  };

  return (
    <div className="min-h-[100dvh] bg-gradient-to-br from-emerald-50 to-indigo-50 p-6">
      <div className="mx-auto max-w-5xl space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-2xl font-bold">Disease Check (Demo)</h3>
          <Button className="bg-slate-700 hover:bg-slate-800" onClick={() => navigate(Routes.DASH)}>Back</Button>
        </div>
        <Card>
          <p className="text-slate-700">Upload a leaf photo (demo runs a fake classifier). Replace this with your ML endpoint later.</p>
          <input type="file" accept="image/*" className="mt-3" onChange={handleUpload} />
        </Card>
        {file && (
          <Card>
            <div className="flex items-start gap-4">
              <img src={URL.createObjectURL(file)} alt="preview" className="w-40 h-40 object-cover rounded-2xl border" />
              <div>
                <h4 className="text-xl font-bold">Results</h4>
                {!result && <p className="text-slate-600">Analyzing…</p>}
                {result && (
                  <ul className="mt-2 space-y-1">
                    {result.map((r, i) => (
                      <li key={i} className="flex items-center gap-3">
                        <span className="w-28 font-medium">{r.label}</span>
                        <div className="flex-1 bg-slate-200 rounded-full h-2 overflow-hidden">
                          <div className="bg-emerald-500 h-2" style={{ width: `${Number(r.score) * 100}%` }} />
                        </div>
                        <span className="font-mono text-sm tabular-nums">{r.score}</span>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}

// ------------------------------
// App Root
// ------------------------------
export default function App() {
  const { route, navigate } = useRouter(Routes.DASH); // default: DASHBOARD directly (no auth)

  return (
    <div className="min-h-[100dvh] font-sans">
      <AnimatePresence mode="wait">
        {route === Routes.DASH && (
          <motion.div key="dash" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <Dashboard navigate={navigate} />
          </motion.div>
        )}
        {route === Routes.DESIGN && (
          <motion.div key="design" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <DesignEmbed navigate={navigate} />
          </motion.div>
        )}
        {route === Routes.CARE && (
          <motion.div key="care" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <CarePlan navigate={navigate} />
          </motion.div>
        )}
        {route === Routes.DISEASE && (
          <motion.div key="disease" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <DiseaseCheck navigate={navigate} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
