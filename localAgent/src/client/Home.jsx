import { useState } from 'react'
import Navbar from './components/navbar'
import Bubble from './components/bubble'
import './Main.css'

function Home() {
  const [count, setCount] = useState(0);
    return(
    <Navbar/>
    )
}
 export default Home