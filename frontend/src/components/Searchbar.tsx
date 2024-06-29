import { FC, FormEvent, useState } from "react";
import SearchIcon from "../icons/SearchIcon";

export interface SearchBarProps {
    onSearch: (query: string) => void;
}

const SearchBar: FC<SearchBarProps> = ({ onSearch }) => {
    const [query, setQuery] = useState("");

    const handleChange = (e: FormEvent<HTMLInputElement>) => {
        setQuery(e.currentTarget.value);
    };

    const onSubmit = (e: FormEvent) => {
        e.preventDefault();
        onSearch(query);
    };

    return (
        <form
            onSubmit={onSubmit}
            className="flex place-items-center rounded-full focus-within:ring-2 shadow"
        >
            <input
                value={query}
                onChange={handleChange}
                type="text"
                className="h-16 outline-none rounded-l-full md:w-[500px] lg:w-[700px] xl:w-[900px] border-none focus:ring-0 px-6 placeholder-opacity-60
                placeholder-gray-500 text-lg"
                name="search"
                placeholder="search for a fashion item"
            />
            <button
                type="submit"
                className="grid place-items-center bg-indigo-500 w-16 h-16 text-white font-bold rounded-r-full relative"
            >
                <SearchIcon className="w-8 h-8 relative -left-1" />
            </button>
        </form>
    );
};

export default SearchBar;
