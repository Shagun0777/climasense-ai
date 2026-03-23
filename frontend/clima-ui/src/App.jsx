import { useState } from "react";

function App() {
  const [city, setCity] = useState("");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    if (!city) return;

    setLoading(true);
    setData(null);

    try {
      const res = await fetch(`http://127.0.0.1:8000/climate/${city}`);
      const json = await res.json();
      setData(json);
    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  };

  const getAQIStyles = (aqi) => {
    if (aqi > 150) return "bg-red-100 text-red-600";
    if (aqi > 100) return "bg-yellow-100 text-yellow-600";
    return "bg-green-100 text-green-600";
  };

  const getBackground = (aqi) => {
    if (aqi > 150) return "from-red-200 via-red-100 to-white";
    if (aqi > 100) return "from-yellow-200 via-yellow-100 to-white";
    return "from-green-200 via-green-100 to-white";
  };

  return (
    <div className={`min-h-screen bg-gradient-to-br ${data ? getBackground(data.data.aqi) : "from-indigo-100 via-blue-50 to-purple-100"} flex flex-col items-center p-6 transition-all duration-700`}>

      {/* HEADER */}
      <div className="text-center mb-10">
        <h1 className="text-5xl font-bold text-gray-800">
          🌍 Climate Intelligence
        </h1>
        <p className="text-gray-500 mt-2">
          Real-time environmental risk insights
        </p>
      </div>

      {/* SEARCH */}
      <div className="flex gap-3 mb-10">
        <input
          className="px-6 py-4 w-96 rounded-2xl border shadow-lg focus:ring-4 focus:ring-blue-300 outline-none transition"
          placeholder="Enter city (e.g. Delhi)"
          value={city}
          onChange={(e) => setCity(e.target.value)}
        />
        <button
          onClick={fetchData}
          className="bg-blue-600 hover:bg-blue-700 text-white px-7 py-4 rounded-2xl shadow-xl transition"
        >
          Search
        </button>
      </div>

      {/* LOADING */}
      {loading && (
        <div className="text-center space-y-3">

          <p className="animate-pulse">🌐 Fetching real-time data...</p>
          <p className="animate-pulse delay-100">🌫️ Analyzing air quality...</p>
          <p className="animate-pulse delay-200">📊 Calculating risk score...</p>
          <p className="animate-pulse delay-300">❤️ Generating health insights...</p>

        </div>
      )}

      {/* DASHBOARD */}
      {data && !loading && (
        <div className="grid md:grid-cols-2 gap-6 w-full max-w-5xl">

          {/* AQI CARD */}
          <div className="bg-white/70 backdrop-blur-lg p-6 rounded-2xl shadow-lg border border-white/30 hover:shadow-[0_0_40px_rgba(0,0,0,0.2)] transition-all duration-500">
            <div className="text-center">
              <p className="text-gray-500">AQI</p>

            <div className={`text-8xl font-extrabold mt-4 px-8 py-4 rounded-3xl inline-block ${getAQIStyles(data.data.aqi)} shadow-2xl animate-pulse`}>                {data.data.aqi}
              </div>
            </div>

            <p className="mt-4 text-gray-600">
              Risk: <span className={`font-semibold ${data.risk.overallRisk === "High" ? "text-red-600" : data.risk.overallRisk === "Medium" ? "text-yellow-600" : "text-green-600"}`}>{data.risk.overallRisk}</span>
            </p>

            <p className="text-gray-500 mt-1">
              {data.trend}
            </p>
          </div>

          {/* ALERT CARD */}
          {data.alert.alert && (
            <div className="bg-red-50 p-6 rounded-2xl shadow-xl border border-red-200 border-l-4 border-l-red-500">
              <h2 className="text-lg font-semibold text-red-600 mb-2">
                ⚠️ Alert
              </h2>
              <p className="text-red-700">{data.alert.message}</p>
            </div>
          )}

          {/* HEALTH */}
          <div className="bg-white/70 backdrop-blur-lg p-6 rounded-2xl shadow-lg border border-white/30 hover:scale-105 hover:shadow-2xl transition-all duration-500 animate-fadeIn">
            <h2 className="text-lg font-semibold mb-2">❤️ Health Impact</h2>
            <p className="text-gray-600">{data.healthImpact}</p>
          </div>

          {/* RECOMMENDATIONS */}
          <div className="bg-white/70 backdrop-blur-lg p-6 rounded-2xl shadow-lg border border-white/30 hover:scale-105 hover:shadow-2xl transition-all duration-500 animate-fadeIn">            <h2 className="text-lg font-semibold mb-2">📋 Recommendations</h2>
            <ul className="space-y-2">
              {data.recommendations.map((rec, i) => (
                <li key={i} className="bg-gray-100 px-4 py-3 rounded-xl shadow-sm hover:bg-gray-200 transition">
                  ✔ {rec}
                </li>
              ))}
            </ul>
          </div>

        </div>
      )}
    </div>
  );
}

export default App;