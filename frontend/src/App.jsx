import { useState, createContext } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { BookOpen, Plane, Hotel, Cloud, ArrowRight, MapPin, Search } from 'lucide-react';
import { agentApi } from './lib/api';
import ReactMarkdown from 'react-markdown';

// --- Context ---
export const TripContext = createContext();

// --- Components ---

const Landing = () => {
    const [source, setSource] = useState("");
    const navigate = useNavigate();

    return (
        <div className="h-screen w-full bg-primary flex items-center justify-center relative overflow-hidden">
            <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?q=80&w=2021&auto=format&fit=crop')] bg-cover bg-center opacity-40"></div>

            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="z-10 bg-glass-panel p-10 rounded-2xl glass-panel w-[500px] text-center"
            >
                <h1 className="text-4xl font-bold mb-2">Trip Spirit</h1>
                <p className="text-slate-300 mb-8">Start your journey.</p>

                <div className="relative">
                    <MapPin className="absolute left-4 top-4 text-slate-400" size={20} />
                    <input
                        type="text"
                        placeholder="Where are you starting from?"
                        className="w-full bg-slate-800/50 border border-slate-600 rounded-xl py-4 pl-12 pr-4 text-white focus:outline-none focus:border-secondary transition-colors"
                        value={source}
                        onChange={(e) => setSource(e.target.value)}
                    />
                </div>

                <button
                    onClick={() => {
                        if (source) {
                            localStorage.setItem("source", source);
                            navigate("/map");
                        }
                    }}
                    className="mt-6 w-full bg-secondary hover:bg-orange-600 text-white font-semibold py-4 rounded-xl flex items-center justify-center gap-2 transition-all"
                >
                    Begin Adventure <ArrowRight size={20} />
                </button>
            </motion.div>
        </div>
    );
};

const MapView = () => {
    const [query, setQuery] = useState("");
    const [places, setPlaces] = useState([]);
    const [selectedPlace, setSelectedPlace] = useState(null);
    const [loading, setLoading] = useState(false);
    const [details, setDetails] = useState(null);

    const handleSearch = async () => {
        setLoading(true);
        if (!query) return;

        try {
            const results = await agentApi.searchPlaces(query);
            if (results && results.length > 0) {
                setPlaces(results);
            } else {
                alert("No places found!");
            }
        } catch (e) {
            console.error(e);
        }
        setLoading(false);
    };

    const handleMarkerClick = async (place) => {
        setSelectedPlace(place);
        setDetails(null);
        // Fetch Agent Insights
        const source = localStorage.getItem("source") || "Unknown";
        const res = await agentApi.invoke(`Analyze ${place.name} for a tourist. Check Weather.`, {
            source,
            destination: place.name,
            place_context: place.name
        });
        setDetails(res.response); // Expecting text response from Agent
    };

    const handleFlights = async () => {
        if (!selectedPlace) return;
        setDetails(null); // Show loading
        const source = localStorage.getItem("source") || "Unknown";
        const res = await agentApi.invoke(`Check flights from ${source} to ${selectedPlace.name}`, {
            source,
            destination: selectedPlace.name,
            place_context: selectedPlace.name
        });
        setDetails(res.response);
    };

    const handleHotels = async () => {
        if (!selectedPlace) return;
        setDetails(null); // Show loading
        const res = await agentApi.invoke(`Find hotels in ${selectedPlace.name}`, {
            source: localStorage.getItem("source") || "Unknown",
            destination: selectedPlace.name,
            place_context: selectedPlace.name
        });
        setDetails(res.response);
    };

    return (
        <div className="h-screen w-full relative">
            <div className="absolute top-0 left-0 right-0 z-[1000] p-4 flex justify-between items-start pointer-events-none">
                <div className="glass-panel px-6 py-3 rounded-full pointer-events-auto flex items-center gap-3">
                    <span className="text-slate-400 text-sm">Start: {localStorage.getItem("source") || "..."}</span>
                    <div className="h-4 w-px bg-slate-600"></div>
                    <Search size={18} className="text-secondary" />
                    <input
                        className="bg-transparent border-none focus:outline-none text-white w-64"
                        placeholder="Where to next? (e.g. Coorg)"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                    />
                </div>
            </div>

            <MapContainer center={[20.5937, 78.9629]} zoom={5} className="h-full w-full bg-slate-900">
                <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                />
                {places.map((p, idx) => (
                    <Marker key={idx} position={[p.lat, p.lon]} eventHandlers={{ click: () => handleMarkerClick(p) }}>
                        <Popup>{p.name}</Popup>
                    </Marker>
                ))}
            </MapContainer>

            <AnimatePresence>
                {selectedPlace && (
                    <motion.div
                        initial={{ x: "100%" }}
                        animate={{ x: 0 }}
                        exit={{ x: "100%" }}
                        transition={{ type: "spring", stiffness: 300, damping: 30 }}
                        className="absolute top-0 right-0 h-full w-[400px] glass-panel z-[1001] p-6 shadow-2xl flex flex-col"
                    >
                        <div className="flex justify-between items-center mb-6">
                            <h2 className="text-2xl font-bold">{selectedPlace.name}</h2>
                            <button onClick={() => setSelectedPlace(null)} className="text-slate-400 hover:text-white">✕</button>
                        </div>


                        <div className="flex-1 overflow-y-auto space-y-4">
                            {!details ? (
                                <div className="flex items-center gap-2 text-secondary animate-pulse">
                                    <Cloud size={20} /> <span className="text-sm">Consulting Trip Spirit...</span>
                                </div>
                            ) : (
                                <div className="prose prose-invert prose-sm max-w-none">
                                    <div className="bg-white/5 p-4 rounded-lg border border-white/10 mb-4">
                                        <ReactMarkdown>{details}</ReactMarkdown>
                                    </div>
                                </div>
                            )}
                        </div>

                        <div className="mt-auto grid grid-cols-2 gap-3 pt-4 border-t border-white/10">
                            <button onClick={handleFlights} className="bg-secondary/20 hover:bg-secondary/40 text-secondary border border-secondary/50 py-3 rounded-lg flex items-center justify-center gap-2 transition-all">
                                <Plane size={18} /> Flights
                            </button>
                            <button onClick={handleHotels} className="bg-blue-500/20 hover:bg-blue-500/40 text-blue-400 border border-blue-500/50 py-3 rounded-lg flex items-center justify-center gap-2 transition-all">
                                <Hotel size={18} /> Hotels
                            </button>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Landing />} />
                <Route path="/map" element={<MapView />} />
            </Routes>
        </Router>
    );
}

export default App;
