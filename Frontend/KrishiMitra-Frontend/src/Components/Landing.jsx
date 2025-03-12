import Navbar from "./Navbar.jsx";
import SecondaryContainer from "./SecondaryContainer.jsx";
import Footer from "./Footer.jsx";

const Landing=()=>{
    return (
        <div className={'min-h-screen w-screen  text-white '}>
            <Navbar/>
            <div className="w-full aspect-video pt-[20%] flex flex-col items-center  absolute text-white bg-gradient-to-t from-black">
                <h1 className=" text-2xl md:text-7xl font-bold font-montserrat">KrishiMitra</h1>
                <p className="hidden md:inline-block py-6 text-lg w-1/2 text-center">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ad, amet, aut beatae blanditiis deleniti ducimus eaque illum molestiae molestias officiis quae, qui quisquam quos repellat saepe unde voluptatum! Inventore, totam!</p>
            </div>

            <div className="-my-4">
                <iframe
                    className="w-full aspect-video"
                    src={"https://www.youtube.com/embed/kQWAXuP0pik?&autoplay=1&mute=1&loop=1&controls=0&playlist=kQWAXuP0pik"}
                    title="YouTube video player"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; "
                    referrerPolicy="strict-origin-when-cross-origin" >
                </iframe>
            </div>
            <SecondaryContainer/>
            <Footer/>

        </div>
    )
}
export default Landing