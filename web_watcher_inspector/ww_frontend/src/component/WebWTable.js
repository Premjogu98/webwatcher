import React from 'react';
import styled from 'styled-components';
import { useTable, usePagination } from 'react-table';
import { useQuery } from 'react-query';
import { getData, globalVariables } from '../globalVariables/global';
import "./WebWTable.css"
import { FetchAdditionalInfo } from '../apiManagement/apiService';
import axios from 'axios';
const columns = [
    {
        Header: "Options",
        accessor: "Options"
    },
    {
        Header: "Sr",
        accessor: "sr_no"
    },
    // {
    //     "Header": "Id",
    //     "accessor": "id"
    // },
    // {
    //     Header: "Tlid",
    //     accessor: "tlid"
    // },
    // {
    //     Header: "Compare Per",
    //     accessor: "compare_per"
    // },
    {
        Header: "Tender Link",
        accessor: "tender_link"
    },
    {
        Header: "Compare_Error",
        accessor: "compare_error"
    },
    {
        Header: "Added_On",
        accessor: "added_on"
    }
    // {
    //     Header: "More",
    //     accessor: "More"
    // },
];
const trimData = (data = []) =>
    data.map(({ name, url }) => ({
        name,
        url,
    }));


const initialState = {
    queryPageIndex: 0,
    queryPageSize: 10,
    totalCount: null,
};

const PAGE_CHANGED = 'PAGE_CHANGED';
const PAGE_SIZE_CHANGED = 'PAGE_SIZE_CHANGED';
const TOTAL_COUNT_CHANGED = 'TOTAL_COUNT_CHANGED';

const reducer = (state, { type, payload }) => {
    switch (type) {
        case PAGE_CHANGED:
            return {
                ...state,
                queryPageIndex: payload,
            };
        case PAGE_SIZE_CHANGED:
            return {
                ...state,
                queryPageSize: payload,
            };
        case TOTAL_COUNT_CHANGED:
            return {
                ...state,
                totalCount: payload,
            };
        default:
            throw new Error(`Unhandled action type: ${type}`);
    }
};
function Modal({ data, shown, close }) {
    console.log(data)
    return data && shown ? (

        <div
            className="modal-backdrop"
            onClick={() => {
                // close modal when outside of modal is clicked
                close();
            }}
        >
            <div
                className="modal-content"
                onClick={e => {
                    // do not close modal if anything inside modal content is clicked
                    e.stopPropagation();
                }}
            >
                <div>
                    <div className='closing-d'><button onClick={close} className='close-button'>X</button></div>
                    <div>
                        <table>
                            <tbody>
                                {
                                    Object.entries(data.detail)
                                        .map(([key, value]) => {
                                            if (key == "Url") {
                                                return (<tr><td>{key}</td><td><a href={value}>{value}</a></td></tr>)
                                            }
                                            return (<tr><td>{key}</td><td>{value}</td></tr>)
                                        })
                                }
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    ) : null;
}
function WebWTable() {
    const [{ queryPageIndex, queryPageSize, totalCount }, dispatch] =
        React.useReducer(reducer, initialState);

    const [isLoading, setIsLoading] = React.useState(true);
    const [error, setError] = React.useState(null);
    const [data, setData] = React.useState(null);
    const [isSuccess, setIsSuccess] = React.useState(false);
    const [modalShown, toggleModal] = React.useState(false);
    const [getselectedData, setSelectedData] = React.useState(null);
    const [getlink, setlink] = React.useState(null);

    React.useEffect(() => {
        const fetchData = async () => {
        try {
            setIsLoading(true);
            const result = await getData(queryPageIndex, queryPageSize);
            console.log(result)
            setData(result);
            setIsSuccess(true);
        } catch (error) {
            setError(error);
        } finally {
            setIsLoading(false);
        }
        };
    
        fetchData();
    }, [queryPageIndex, queryPageSize]);

    // const { isLoading, error, data, isSuccess } = useQuery(
    //     ['pokemons', queryPageIndex, queryPageSize],
    //     () => getData(queryPageIndex, queryPageSize),
    //     {
    //         keepPreviousData: true,
    //         staleTime: Infinity,
    //     }
    // );
    

    const FetchAdditionalInfo1 = async (id) => {
        try {
            const main_url = `${globalVariables.apiUrl}/addition/data?id=${id}`
            const response = await axios.get(main_url);
            console.log(response.data)
            setSelectedData(response.data)
        } catch (error) {
            console.error("Error fetching data:", error);
            throw error;
        }
    }
    const handleButtonClick = (value, modalState) => {
        toggleModal(modalState)
        console.log(value)
        FetchAdditionalInfo1(value)

    };
    const changeInput = (e) => {
        setlink(e.target.value);
    };

    const getsearchdata = async () => {
        try {
            setIsLoading(true);
            const result = await getData(queryPageIndex, queryPageSize,getlink);
            console.log(result)
            setData(result);
            setIsSuccess(true);
        } catch (error) {
            setError(error);
        } finally {
            setIsLoading(false);
        }
        };
    const {
        getTableProps,
        getTableBodyProps,
        headerGroups,
        prepareRow,
        page,
        canPreviousPage,
        canNextPage,
        pageOptions,
        pageCount,
        gotoPage,
        nextPage,
        previousPage,
        setPageSize,
        // Get the state from the instance
        state: { pageIndex, pageSize },
    } = useTable(
        {
            columns,
            data: isSuccess ? data.detail.data : [],
            initialState: {
                pageIndex: queryPageIndex,
                pageSize: queryPageSize,
            },
            manualPagination: true,
            pageCount: isSuccess ? Math.ceil(data.detail.count / queryPageSize) : null,
        },
        usePagination
    );

    React.useEffect(() => {
        dispatch({ type: PAGE_CHANGED, payload: pageIndex });
    }, [pageIndex]);

    React.useEffect(() => {
        dispatch({ type: PAGE_SIZE_CHANGED, payload: pageSize });
        gotoPage(0);
    }, [pageSize, gotoPage]);

    React.useEffect(() => {
        if (data?.count) {
            dispatch({
                type: TOTAL_COUNT_CHANGED,
                payload: data.count,
            });
        }
    }, [data?.count]);

    if (error) {
        return <p>Error</p>;
    }

    if (isLoading) {
        return <p>Loading...</p>;
    }
    let sr = 0;
    return (
        <div id='record-table'>
            {isSuccess ? (
                <>
                    <div class="table-filter">
                        <div className='filter-d'><label>Tender link</label> <input className='search' onChange={changeInput}></input> <button className='search-btn' onClick={getsearchdata}> search </button></div>
                    </div>
                    <table {...getTableProps()}>
                        <thead>
                            {headerGroups.map((headerGroup) => (
                                <tr {...headerGroup.getHeaderGroupProps()}>
                                    {headerGroup.headers.map((column) => (
                                        <th {...column.getHeaderProps()}>
                                            {column.render('Header')}
                                        </th>
                                    ))}
                                </tr>
                            ))}
                        </thead>
                        <tbody {...getTableBodyProps()}>
                            {page.map((row) => {
                                prepareRow(row);
                                sr++;
                                return (
                                    <tr {...row.getRowProps()}>


                                        {row.cells.map((cell) => {
                                            { console.log(cell) }

                                            if (cell.column.Header == "Tender Link") {
                                                return (
                                                    <td><a href={cell.value} target='/' style={{ "color": 'darkcyan', "text-decoration": 'none' }}>{cell.value}</a></td>
                                                );
                                            } else if (cell.column.Header == "Compare_Error") {
                                                return (
                                                    <td className='error'>{cell.value}</td>
                                                )
                                            } else if (cell.column.Header == "Sr") {
                                                return (
                                                    <td>{sr}</td>
                                                )
                                            } else if (cell.column.Header == "Options") {
                                                return (
                                                    <td>
                                                        <a href={"/inspect/" + cell.row.original.id} className='view-more inspect-btn'>inspect</a>&nbsp;
                                                        {/* <button className='view-more' onClick={() => handleButtonClick(row.original.id, !modalShown)}>view more</button>&nbsp; */}
                                                    </td>
                                                )
                                            } else {
                                                return (<td>{cell.value}</td>)
                                            }

                                        })}

                                    </tr>
                                );

                            })}
                        </tbody>
                    </table>
                    <Modal data={getselectedData} shown={modalShown} close={() => { toggleModal(false); }} />
                    <ul className="pagination">
                        <li onClick={() => gotoPage(0)} className={canPreviousPage ? "active" : "disable"}>
                            {'First'}
                        </li>{' '}
                        <li onClick={() => previousPage()} className={canPreviousPage ? "active" : "disable"}>
                            {'Previous'}
                        </li>{' '}
                        <li onClick={() => nextPage()} className={canNextPage ? "active" : "disable"}>
                            {'Next'}
                        </li>{' '}
                        <li
                            onClick={() => gotoPage(pageCount - 1)}
                            className={canNextPage ? "active" : "disable"}
                        >
                            {'Last'}
                        </li>{' '}
                        <li><span>
                            Page{' '}
                            <strong>
                                {pageIndex + 1} of {pageOptions.length}
                            </strong>{' '}
                        </span>
                        </li>

                        <li>
                            | Go to page:{' '}
                            <input
                                type="number"
                                value={pageIndex + 1}
                                onChange={(e) => {
                                    const page = e.target.value ? Number(e.target.value) - 1 : 0;
                                    gotoPage(page);
                                }}
                            />
                        </li>{' '}
                        {/* <li>
                            <select
                                value={pageSize}
                                onChange={(e) => {
                                    setPageSize(Number(e.target.value));
                                }}
                            >
                                {[10, 20, 30, 40, 50].map((pageSize) => (
                                    <option key={pageSize} value={pageSize}>
                                        Show {pageSize}
                                    </option>
                                ))}
                            </select>
                        </li> */}
                    </ul>

                </>
            ) : null}
        </div>
    );
}

export default WebWTable;
