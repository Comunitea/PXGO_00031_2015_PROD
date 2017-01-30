from openerp import models, fields, tools, api, exceptions, _


class ParticularReport(models.AbstractModel):
    _name = 'report.mrp.report_mrporder'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name(
            'mrp.report_mrporder') 
		

        dic_locations = {}
        for docu in self.env[report.model].browse(self._ids): 
            dic = {}            
            for stock_move_line in docu.move_lines: 
                dic[stock_move_line.id] = {}             
                for stock_quant_line in stock_move_line.reserved_quant_ids: 
                    if stock_quant_line.location_id.complete_name not in dic[stock_move_line.id]: 
                        dic[stock_move_line.id][stock_quant_line.location_id.complete_name] = stock_quant_line.qty 
                        print 'if', dic
                    else:
                        dic[stock_move_line.id][stock_quant_line.location_id.complete_name] += stock_quant_line.qty
                        print 'else', dic
                    print dic


            dic_locations[docu.id] = dic   


        print 'dic_locations: ', dic_locations
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self.env[report.model].browse(self._ids),
            'dic_locations': dic_locations,
        }
        return report_obj.render('mrp.report_mrporder',
                                 docargs)



