SELECT * FROM `tend_dms`.`dms_wpw_tenderlinksdata` where Url="https://nji.gov.ng/rfq/";
SELECT * FROM `tend_dms`.`dms_wpw_tenderlinksdata` where tlid=71112;

SELECT data.id, data.tlid, data.title, data.XPath, data.compare_per, data.CompareChangedOn, data.oldHtmlPath, data.newHtmlPath, data.oldImagePath, data.newImagePath, data.CompareBy, data.LastCompareChangedOn,links.tender_link FROM `tend_dms`.`dms_wpw_tenderlinks` links INNER JOIN `tend_dms`.`dms_wpw_tenderlinksdata` data ON links.id = data.tlid INNER JOIN tbl_region re ON links.country = re.Country_Short_Code WHERE data.tlid = 71112;

SELECT data.id, data.tlid, data.title, data.XPath, data.compare_per, data.CompareChangedOn, data.oldHtmlPath, data.newHtmlPath, data.oldImagePath, data.newImagePath, data.CompareBy, data.LastCompareChangedOn,links.tender_link FROM `tend_dms`.`dms_wpw_tenderlinks` links INNER JOIN `tend_dms`.`dms_wpw_tenderlinksdata` data ON links.id = data.tlid INNER JOIN tbl_region re ON links.country = re.Country_Short_Code WHERE links.process_type = 'Web Watcher' AND links.added_WPW = 'Y' AND data.entrydone = 'Y' AND (re.Region_Code LIKE '101%' OR re.Region_Code LIKE '102%' OR re.Region_Code LIKE '104%' OR re.Region_Code LIKE '105%' OR re.Region_Code LIKE '103304%') ORDER BY links.id ASC LIMIT 10 OFFSET 0;


SELECT COUNT(*) AS record_count
FROM dms_wpw_tenderlinks tl 
INNER JOIN dms_wpw_tenderlinksdata td ON tl.id = td.tlid
INNER JOIN tbl_region re ON tl.country = re.Country_Short_Code
WHERE tl.process_type = 'Web Watcher' AND tl.added_WPW = 'Y'
ORDER BY tl.id ASC