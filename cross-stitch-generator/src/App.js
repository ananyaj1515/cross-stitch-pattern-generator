import logo from './logo.svg';
import './App.css';
import { useState } from 'react';


function App() {

  const [image, setImage] = useState(null)
  const [maxDim, setMaxDim] = useState(50)
  const [nColors, setNColors] = useState(15)
  const [patternData, setPatternData] = useState(null)
  const [loading , setLoading] = useState(false)

  const handleImageUpload = (e) => {
    setImage(e.target.files[0]);
  };

  const handleProcess = async() => {
    if (!image) return

    setLoading(true)
    const formData = new FormData()
    formData.append('image', image)
    formData.append('max_dim', maxDim)
    formData.append('n_colors', nColors)

    try {
      const response = await fetch('http://127.0.0.1:5000/process', {
        method: 'POST',
        body: formData
      })

      const data = await response.json()
      setPatternData(data)

    } catch (err) {
      console.log("Error", err)
    } finally {
      setLoading(false)

    }
  }
  return (
    <div className='App'>
      <h1>Cross-Stich Pattern Generator</h1>
      <input type='file' accept='image/*' onChange={handleImageUpload}/>
      <div>
        <label>Grid Size: {maxDim}</label>
        <input type="range" min="20" max="100" value={maxDim} onChange={(e) => setMaxDim(e.target.value)}/>
      </div>
      <div>
        <label>Number of Colours: {nColors}</label>
        <input type="range" min="5" max="30" value={nColors} onChange={(e) => setNColors(e.target.value)}/>
      </div>
      <button onClick={handleProcess} disabled={!image || loading}>
        {loading ? 'Processing ...' : 'Generate Pattern'}
      </button>

      {patternData && (
  <div className="pattern-container">
    <div className="pattern-grid">
      {patternData.pattern_grid.map((row, rowIndex) => (
        <div key={rowIndex} className="pattern-row">
          {row.map((dmcCode, colIndex) => {
            const colorInfo = patternData.key[dmcCode];
            return (
              <div 
  key={`${rowIndex}-${colIndex}`}
  className="stitch-cell"
  style={{ 
    color: `rgb(${colorInfo.rgb.join(',')})` // Color the cross, not background
  }}
  title={`${dmcCode} - ${colorInfo.name}`}
>
  ✕
</div>
            );
          })}
        </div>
      ))}
    </div>
  </div>
)}
    </div>
  )
}

export default App;
