import { useState } from "react";
import SearchBar from "./components/Searchbar";

export type SearchResponse = Array<{
    id: string;
    link: string;
    similarity: number;
}>;

const search = async (query: string): Promise<SearchResponse | null> => {
    console.log(query);
    const searchParams = new URLSearchParams();
    searchParams.append("q", query);

    const response = await fetch(
        `http://localhost:5000/search?${searchParams.toString()}`
    );

    if (!response.ok) {
        console.error("Failed to search");
        return null;
    }

    return await response.json();
};

function App() {
    const [searchResults, setSearchResults] = useState<SearchResponse>([]);
    const [isLoading, setIsLoading] = useState(false);

    const handleSearch = async (query: string) => {
        setIsLoading(true);
        const data = await search(query);
        setSearchResults(data as SearchResponse);
        setIsLoading(false);
    };

    return (
        <>
            <h1 className="text-6xl text-center p-5">Fashion Finder</h1>

            <div className="grid justify-center mb-5">
                <SearchBar onSearch={handleSearch} />
            </div>

            {isLoading && <p className="text-center">Loading...</p>}
            {!isLoading && (
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
            )}
        </>
    );
}

export default App;
