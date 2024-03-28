import React from 'react';
root.render(
    <BrowserRouter>

        <Routes>
            <Route index element={<Home />} />
            <Route path='/app' element={<App />} />
        </Routes>
    </BrowserRouter>
);