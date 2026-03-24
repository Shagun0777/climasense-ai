import { useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { Cell } from "recharts";

function App() {
  const [city, setCity] = useState("");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [asking, setAsking] = useState(false);

  const fetchData = async () => {
    if (!city) return;

    setLoading(true);
    setData(null);
    setAnswer("");    
    setQuestion("");

    try {
      const res = await fetch(`http://127.0.0.1:8000/climate/${city}`);
      const json = await res.json();
      setData(json);
      console.log("API RESPONSE:", json);
    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  };

  const askQuestion = async (customQuestion) => {
    const finalQuestion = customQuestion || question;

    if (!finalQuestion || !city) return;

    setAsking(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          question: finalQuestion,
          city
        })
      });

      const json = await res.json();
      setAnswer(json.answer);
    } catch (err) {
      console.error(err);
    }

    setAsking(false);
  };

  const getAQIStyles = (aqi) => {
    if (aqi <= 50) return "bg-green-100 text-green-600";
    if (aqi <= 100) return "bg-yellow-100 text-yellow-600";
    if (aqi <= 150) return "bg-orange-100 text-orange-600";
    if (aqi <= 200) return "bg-red-100 text-red-600";
    return "bg-purple-100 text-purple-700";
  };

  const getBackground = (aqi) => {
    if (aqi <= 50) return "from-green-300 via-green-100 to-white";
    if (aqi <= 100) return "from-yellow-300 via-yellow-100 to-white";
    if (aqi <= 150) return "from-orange-300 via-orange-100 to-white";
    if (aqi <= 200) return "from-red-300 via-red-100 to-white";
    return "from-purple-400 via-red-200 to-white";
  };

  const labelMap = {
    pm2_5: "Fine Dust",
    pm10: "Dust",
    no2: "Traffic Gas",
    o3: "Ozone"
  };

  const chartData = data?.data?.components
    ? Object.entries(data.data.components)
        .filter(([key]) => ["pm2_5", "pm10", "no2", "o3"].includes(key))
        .map(([key, value]) => {
          const level = data.data.levels?.[key] || "Unknown";

          return {
            name: labelMap[key],
            value: Math.round(value),
            level
          };
        })
    : [];

  const getBarColor = (level) => {
    if (level === "Good") return "#22c55e";
    if (level === "Moderate") return "#eab308";
    if (level === "Unhealthy") return "#f97316";
    if (level === "Severe") return "#ef4444";
    return "#94a3b8";
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
          onKeyDown={(e) => {if (e.key === "Enter") fetchData();}}
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
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-5xl">

          {/* AQI CARD */}
          <div className="bg-white/70 backdrop-blur-lg p-6 rounded-2xl shadow-lg border border-white/30 hover:shadow-[0_0_40px_rgba(0,0,0,0.2)] transition-all duration-500">
            <div className="text-center">
              <p className="text-gray-500">AQI</p>

            <div className={`text-8xl font-extrabold mt-4 px-8 py-4 rounded-3xl inline-block ${getAQIStyles(data.data.aqi)} shadow-2xl animate-pulse`}>                {data.data.aqi}
              </div>
            </div>

            <p className={`mt-2 inline-block px-3 py-1 rounded-full font-semibold ${
                data.data.aqi <= 50 ? "bg-green-200 text-green-800" :
                data.data.aqi <= 100 ? "bg-yellow-200 text-yellow-800" :
                data.data.aqi <= 150 ? "bg-orange-200 text-orange-800" :
                data.data.aqi <= 200 ? "bg-red-200 text-red-800" :
                "bg-purple-200 text-purple-800"
              }`}>
              {data.data.aqi <= 50 && "Good"}
              {data.data.aqi <= 100 && data.data.aqi > 50 && "Moderate"}
              {data.data.aqi <= 150 && data.data.aqi > 100 && "Unhealthy (Sensitive)"}
              {data.data.aqi <= 200 && data.data.aqi > 150 && "Unhealthy"}
              {data.data.aqi > 200 && "Severe"}
            </p>

            <p className="mt-4 text-gray-600">
              Risk: <span className={`font-semibold ${data.risk.overallRisk === "High" ? "text-red-600" : data.risk.overallRisk === "Medium" ? "text-yellow-600" : "text-green-600"}`}>{data.risk.overallRisk}</span>
            </p>

            <p className="text-gray-500 mt-1">
              {data.trend}
            </p>

            <p className="text-sm mt-2 text-gray-600">
              Dominant: <b>{data.data.dominantPollutant}</b>
            </p>

            <p className="text-sm text-gray-600">
              Source: <b>{data.data.pollutionSource}</b>
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

          {/* AI INSIGHT */}
          <div className="bg-purple-100 p-6 rounded-2xl shadow-lg border border-purple-200 col-span-2">
            <h2 className="text-lg font-semibold text-purple-700 mb-2">
              🧠 AI Insight
            </h2>
            <p className="mt-2 text-sm text-gray-600"> 📊 Generated using real-time data, trend analysis, and AI reasoning</p>
            <p><b>Summary:</b> {data?.aiInsight?.summary || "No insight available"}</p>
            <p><b>Cause:</b> {data?.aiInsight?.cause || "N/A"}</p>
            <p><b>Outlook:</b> {data?.aiInsight?.riskOutlook || "N/A"}</p>
            <p><b>Confidence:</b> {data?.aiInsight?.confidence || "N/A"}</p>
          </div>

          {/* RECOMMENDATIONS */}
          <div className="bg-white/70 backdrop-blur-lg p-6 rounded-2xl shadow-lg border border-white/30 hover:scale-105 hover:shadow-2xl transition-all duration-500 animate-fadeIn">            <h2 className="text-lg font-semibold mb-2">📋 Recommendations</h2>
            <ul className="space-y-2">
              {data.recommendations.map((rec, i) => (
                <li key={i} className="bg-gray-100 px-4 py-3 rounded-xl shadow-sm hover:bg-gray-200 transition">
                 <li key={i} className="bg-gray-100 px-4 py-3 rounded-xl shadow-sm"><span className="font-medium">✔ {rec}</span></li>
                </li>
              ))}
            </ul>
          </div>

          {/* POLLUTION CHART */}
          <div className="bg-white/70 backdrop-blur-lg p-6 rounded-2xl shadow-lg border border-white/30 col-span-2">
            <h2 className="text-lg font-semibold mb-4">📊 Pollution Breakdown</h2>

            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={chartData}>
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip formatter={(value, name, props) => [`${value} (${props.payload.level})`,"Level" ]}/>
                <Bar dataKey="value" radius={[10, 10, 0, 0]}>{chartData.map((entry, index) => (<Cell key={`cell-${index}`} fill={getBarColor(entry.level)} />))}</Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* AI CHAT PANEL */}
          <div className="bg-white/80 backdrop-blur-lg p-6 rounded-2xl shadow-lg border border-white/30 col-span-2 mt-4">
            <h2 className="text-lg font-semibold mb-3">💬 Ask AI</h2>

            <div className="flex gap-2">
              <input
                className="flex-1 px-4 py-3 rounded-xl border focus:ring-2 focus:ring-blue-300 outline-none"
                placeholder="Ask something like: Can I go for a run?"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyDown={(e) => {if (e.key === "Enter") askQuestion();}}
              />
              <button
                onClick={askQuestion}
                className="bg-purple-600 text-white px-5 py-3 rounded-xl hover:bg-purple-700"
              >
                Ask
              </button>
            </div>

            {asking && (
              <p className="mt-3 text-sm text-gray-500 animate-pulse">
                🤖 Thinking...
              </p>
            )}

            <div className="mt-3 flex flex-wrap gap-2">

            {[
              "Can I go outside today?",
              "Is it safe for kids?",
              "Why is pollution high?",
              "Should I wear a mask?"
            ].map((q, i) => (
              <button
                key={i}
                onClick={() => {setQuestion(q); askQuestion(q);}}
                className="text-xs bg-gray-200 px-3 py-1 rounded-full hover:bg-gray-300"
              >
                {q}
              </button>
            ))}
          </div>

            {answer && !asking && (
              <div className="mt-4 bg-gradient-to-r from-purple-50 to-blue-50 p-4 rounded-xl border">
                <p className="text-gray-700">{answer}</p>
              </div>
            )}
          </div>

        </div>
      )}
    </div>
  );
}

export default App;