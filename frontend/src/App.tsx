import { useState } from "react";
import SearchBar, { SearchResponse } from "./components/Searchbar";

function App() {
    const [searchResults, setSearchResults] = useState<SearchResponse>([]);

    const onResults = (results: SearchResponse) => {
        setSearchResults(results);
    };

    return (
        <>
            <h1 className="text-6xl text-center p-5">Fashion Finder</h1>

            <div className="grid justify-center mb-5">
                <SearchBar onResults={onResults} />
            </div>

            <div className="grid justify-center">
                <ul className="w-[900px] grid grid-cols-2">
                    {searchResults.map((result) => (
                        <li key={result.id}>
                            <img
                                src={`http://localhost:5000/images/${result.id}`}
                                alt=""
                                width={500}
                            />
                        </li>
                    ))}
                </ul>
            </div>
        </>
    );
}

export default App;
