import { useState } from 'react'
import Bubble from './components/bubble'
import './Main.css'

function Home() {
  const [count, setCount] = useState(0);
    return(<div>
    <Bubble/>
    </div>)
}
 export default Home