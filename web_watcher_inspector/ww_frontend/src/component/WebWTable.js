import React from 'react';
import styled from 'styled-components';
import { useTable, usePagination } from 'react-table';
import { useQuery } from 'react-query';
import { getData } from '../globalVariables/global';
import "./WebWTable.css"

const columns = [
    {
        Header: "Sr",
        accessor: "sr_no"
    },
    // {
    //     Header: "Id",
    //     accessor: "id"
    // },
    {
        Header: "Tlid",
        accessor: "tlid"
    },
    {
        Header: "Title",
        accessor: "title"
    },
    // {
    //     Header: "Xpath",
    //     accessor: "XPath"
    // },
    // {
    //     Header: "Compare Per",
    //     accessor: "compare_per"
    // },
    {
        Header: "Tender_Link",
        accessor: "tender_link"
    },
    {
        Header: "Compared On",
        accessor: "CompareChangedOn"
    },
    {
        Header: "Last Compared On",
        accessor: "LastCompareChangedOn"
    },
    // {
    //     Header: "Newhtmlpath",
    //     accessor: "newHtmlPath"
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

function WebWTable() {
    const [{ queryPageIndex, queryPageSize, totalCount }, dispatch] =
        React.useReducer(reducer, initialState);

    const { isLoading, error, data, isSuccess } = useQuery(
        ['pokemons', queryPageIndex, queryPageSize],
        () => getData(queryPageIndex, queryPageSize),
        {
            keepPreviousData: true,
            staleTime: Infinity,
        }
    );

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

    return (
        <div id='record-table'>
            {isSuccess ? (
                <>
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
                                return (
                                    <tr {...row.getRowProps()}>
                                        
                                        {/* <td> <button>inspect</button></td> */}
                                        {row.cells.map((cell) => {
                                            console.log(cell)
                                            console.log(row.cells)
                                            console.log('Logging information before rendering td:',cell);
                                            console.log(cell.column)
                                            if(cell.column.Header == "Tender_Link"){
                                                return (
                                                    <td><a href={"/inspect/"+cell.row.original.tlid} style={{ "color": 'darkcyan', "text-decoration": 'none' }}>{cell.value}</a></td>
                                                );
                                            }
                                            return (
                                                <td>{cell.value}</td>
                                            );
                                        })}
                                        <td style={{ "border": 'none'}}> <button>+</button></td>
                                        
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
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
                        <li><select
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
                        </li>
                    </ul>
                </>
            ) : null}
        </div>
    );
}

export default WebWTable;
