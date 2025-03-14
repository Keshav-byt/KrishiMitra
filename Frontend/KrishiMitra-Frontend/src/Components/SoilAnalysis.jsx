import Navbar from "./Navbar.jsx";
import {useState} from "react";

const SoilAnalysis = () => {
    const soilMinerals = [
        "Nitrogen",
        "Phosphorus",
        "Potassium",
        "pH",
        "Electrical Conductivity",
        "Organic Carbon",
        "Sulfur",
        "Zinc",
        "Iron",
        "Copper",
        "Manganese",
        "Boron"
    ];

    const [mineralValue, setMineralValue] = useState(
        soilMinerals.reduce((acc,mineral) => {
            acc[mineral]=0;
            return acc;
        },{}),
    );
    const handleChange=(value,mineral)=>{
        setMineralValue((prev)=>({
                ...prev,
                [mineral]:value
        }));
    }
    const handleSubmit=()=>{
        console.log(mineralValue)
    }


    return (
        <div className={'h-screen w-full flex flex-col items-center justify-center bg-[url("https://t3.ftcdn.net/jpg/02/57/58/20/360_F_257582025_LUf6zGRPA0x0OGaLFS1UJIgkRKrrZhAk.jpg")] bg-cover bg-center'}>
            <Navbar />
            <div className={'h-[70%] w-[53%] bg-gradient-to-br from-zinc-800/50 via-zinc-900/50 to-zinc-950/50 backdrop-blur-sm rounded-3xl border border-gray-500 p-10 flex flex-col items-center justify-between text-white'}>
                <h1 className={'text-3xl font-medium mb-3'}>Soil Analysis</h1>
                <div className={'flex items-center w-full h-[85%]'}>
                    <div className={'h-full w-[50%]  p-2.5 flex flex-col items-center justify-between'}>
                        {/*<h1 className={'text-xl'}>Input Data</h1>*/}
                        <div className={'overflow-y-auto w-full h-[80%] '}>
                            {soilMinerals.map ((m)=>(
                                <div key={m} className={'m-1.5 mb-3.5 text-sm'}>
                                    <label>{`Enter value for ${m} `}</label>
                                    <input
                                        type="number"
                                        placeholder={m}
                                        value={mineralValue[m]}
                                        className={'w-[90%] border border-gray-500 rounded p-1 placeholder:text-sm'}
                                        onChange={(e)=>handleChange(e.target.value,m)}
                                    />
                                </div>
                                ))}
                        </div>
                        <button
                            onClick={handleSubmit}
                            className={'px-8 py-2 border-2 border-white rounded-full font-medium my-2'}>Get Fertility</button>
                    </div>
                    <div className={'h-full w-[50%] border-l-2  border-gray-500 flex flex-col items-center justify-center text-center' }>

                        <img src="https://cdni.iconscout.com/illustration/free/thumb/free-searching-data-illustration-download-in-svg-png-gif-file-formats--no-content-yet-for-web-empty-states-pack-design-development-illustrations-3385493.png" alt=""/>
                        <h1
                            className={'px-12 text-sm font-medium '}
                        >Click on 'Get Fertility' To get the result
                        </h1>
                    </div>
                </div>
            </div>
        </div>
    )
}
export default SoilAnalysis