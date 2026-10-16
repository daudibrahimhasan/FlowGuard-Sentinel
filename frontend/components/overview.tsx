'use client';
import {useEffect,useState} from 'react';
import {ArrowRight,CalendarDays,Check,ShieldCheck} from 'lucide-react';
import {api,Dashboard,dateLabel,exactMoney,money} from '@/lib/api';
import {Bar,BarChart,CartesianGrid,ResponsiveContainer,Tooltip,XAxis,YAxis} from 'recharts';
import {Badge,Forecast} from './views';

type AuditEvent={id:number;event:string;timestamp:string;business_id:string|null;details:Record<string,unknown>};
export function Overview({dashboard,identity,onNavigate}:{dashboard:Dashboard;identity:string;onNavigate:(page:string)=>void}){
 const [activity,setActivity]=useState<{events:AuditEvent[];integrity:{valid:boolean}}|null>(null),[error,setError]=useState('');
 useEffect(()=>{let active=true;api<{events:AuditEvent[];integrity:{valid:boolean}}>('/audit',identity).then(v=>{if(active){setActivity(v);setError('')}}).catch(()=>{if(active)setError('Recent activity could not load.')});return()=>{active=false}},[identity,dashboard.business.id,dashboard.current_cash,dashboard.proposals.length]);
 const pending=dashboard.proposals.filter(p=>['proposed','approved'].includes(p.status)).length;
 const outstanding=dashboard.invoices.filter(i=>i.amount>i.paid).sort((a,b)=>b.amount-b.paid-(a.amount-a.paid));
 const expenses=[...dashboard.expenses].sort((a,b)=>a.date.localeCompare(b.date));
 const categories=Object.entries(expenses.reduce<Record<string,number>>((groups,e)=>{groups[e.category]=(groups[e.category]||0)+e.amount;return groups},{})).sort((a,b)=>b[1]-a[1]);
 const spending=expenses.reduce((sum,e)=>sum+e.amount,0);
 const events=activity?.events.filter(e=>e.business_id===dashboard.business.id||e.business_id===null).slice(-3).reverse()||[];
 return <>
  <div className="report-filter-row"><span className="report-period"><CalendarDays size={14}/>17–30 Oct 2026</span><span>14-day forecast · CNY</span><button className="text-button" onClick={()=>onNavigate('Approvals')}>{pending} awaiting review <ArrowRight size={14}/></button></div>
  <div className="reporting-grid">
   <section className="report-panel report-cash">
    <button className="report-title" onClick={()=>onNavigate('Cash-flow analysis')}>Cash position <ArrowRight size={14}/></button>
    <div className="report-cash-stats"><div><span>Available cash</span><strong>{money(dashboard.current_cash)}</strong><small>Confirmed ledger balance</small></div><div><span>Lowest projected balance</span><strong className={dashboard.minimum_balance<0?'cash-warning':''}>{money(dashboard.minimum_balance)}</strong><small>{dashboard.shortfall_date?'First shortfall · '+dateLabel(dashboard.shortfall_date):'No expected shortfall'}</small></div></div>
    <Forecast data={dashboard.forecast}/>
    <div className="report-chart-key"><span><i/>Expected balance</span><span><i/>No additional collections</span></div>
   </section>
   <section className="report-panel report-payments">
    <button className="report-title" onClick={()=>onNavigate('Cash-flow analysis')}>Upcoming obligations <ArrowRight size={14}/></button>
    <p className="report-insight">{dashboard.shortfall_amount>0?`${money(dashboard.shortfall_amount)} cash gap projected ${dashboard.shortfall_date?dateLabel(dashboard.shortfall_date):'within 14 days'}. Payroll stays protected.`:'Expected collections cover scheduled obligations.'}</p>
    <div className="report-inline-stats"><div><span>Scheduled payments</span><strong>{expenses.length}</strong></div><div><span>Total scheduled</span><strong>{money(spending)}</strong></div></div>
    <ol className="ranked-records">{expenses.map((e,i)=><li key={e.id}><span className="rank-number">{i+1}</span><span className={'record-avatar record-avatar-'+i}>{e.vendor.split(' ').map(word=>word[0]).slice(0,2).join('')}</span><span className="ranked-record-name"><strong>{e.vendor}</strong><small>{dateLabel(e.date)} · {e.flexible?'Flexible':'Protected / committed'}</small></span><span className="ranked-record-amount">{exactMoney(e.amount)}</span></li>)}</ol>
   </section>
   <section className="report-panel report-receivables">
    <button className="report-title" onClick={()=>onNavigate('Recovery agent')}>Receivables by customer <ArrowRight size={14}/></button>
    <p className="report-insight">{money(dashboard.overdue_total)} overdue. Customer payment has not been recorded.</p>
    <div className="report-inline-stats"><div><span>Open invoices</span><strong>{outstanding.length}</strong></div><div><span>Total outstanding</span><strong>{money(outstanding.reduce((sum,i)=>sum+i.amount-i.paid,0))}</strong></div></div>
    <div className="receivable-bars">{outstanding.map((invoice,i)=><div key={invoice.id}><div><span>{invoice.customer.replace(' (synthetic)','')}</span><strong>{exactMoney(invoice.amount-invoice.paid)}</strong></div><div className="bar-track"><span className={'bar-fill bar-fill-'+i} style={{width:`${Math.max(1,(invoice.amount-invoice.paid)/Math.max(1,...outstanding.map(v=>v.amount-v.paid))*100)}%`}}/></div></div>)}</div>
   </section>
   <section className="report-panel report-spending">
    <button className="report-title" onClick={()=>onNavigate('Cash-flow analysis')}>Spending by category <ArrowRight size={14}/></button>
    <div className="report-inline-stats"><div><span>Top category</span><strong className="category-label">{categories[0]?.[0]||'No obligations'}</strong></div><div><span>Total scheduled</span><strong>{money(spending)}</strong></div></div>
    <div className="spend-legend">{categories.map(([category],i)=><span key={category}><i className={'category-color-'+i}/>{category}</span>)}</div>
    <div className="category-chart" aria-label="Scheduled obligations by category"><ResponsiveContainer width="100%" height="100%"><BarChart data={[{name:'17–30 Oct',...Object.fromEntries(categories)}]} margin={{top:8,right:12,left:0,bottom:0}}><CartesianGrid vertical={false} stroke="#efefe7"/><XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fontSize:9,fill:'#969687'}}/><YAxis width={44} axisLine={false} tickLine={false} tick={{fontSize:9,fill:'#969687'}} tickFormatter={v=>`¥${v/1000}k`}/><Tooltip formatter={(v:number)=>exactMoney(v)} contentStyle={{fontSize:11,border:'1px solid #e8e8df',borderRadius:0}}/>{categories.map(([category],i)=><Bar key={category} dataKey={category} stackId="scheduled" barSize={78} fill={['#6a7746','#6ca988','#997b9d','#c19378','#8aa2c2'][i%5]} isAnimationActive={false}/>)}</BarChart></ResponsiveContainer></div>
    <p className="report-footnote">Scheduled obligations only. Not historical spending.</p>
   </section>
  </div>
  <section className="report-ledger">
   <div className="report-ledger-heading"><h2>Receivables to follow up <span>{outstanding.length}</span></h2><button className="text-button" onClick={()=>onNavigate('Recovery agent')}>Prepare a collection plan <ArrowRight size={14}/></button></div>
   <div className="table-scroll"><table><thead><tr><th>Customer</th><th>Invoice</th><th>Due date</th><th>Outstanding</th><th>Status</th></tr></thead><tbody>{outstanding.map(i=><tr key={i.id}><td>{i.customer.replace(' (synthetic)','')}</td><td className="mono">{i.id}</td><td>{dateLabel(i.due_date)}</td><td>{exactMoney(i.amount-i.paid)}</td><td><Badge tone={i.due_date<'2026-10-16'?'amber':'neutral'}>{i.due_date<'2026-10-16'?'Overdue':'Upcoming'}</Badge></td></tr>)}</tbody></table></div>
  </section>
  <div className="report-audit-line"><ShieldCheck size={14}/><span>{dashboard.verification.message}</span><button className="text-button" onClick={()=>onNavigate('Audit trail')}>View audit trail <ArrowRight size={14}/></button></div>
  <section className="report-activity"><div className="report-ledger-heading"><h2>Recent activity</h2><button className="text-button" onClick={()=>onNavigate('Audit trail')}>Open audit trail <ArrowRight size={14}/></button></div>{error?<p role="status">{error}</p>:!activity?<p className="muted">Loading recorded activity…</p>:<>{events.map(e=><div className="activity-row" key={e.id}><span className="activity-icon"><Check size={14}/></span><div><strong>{e.event.replaceAll('_',' ')}</strong><small>{String(e.details.actor||'System')} · {new Date(e.timestamp).toLocaleString('en-GB',{timeZone:'Asia/Dhaka',day:'numeric',month:'short',hour:'2-digit',minute:'2-digit'})} Dhaka</small></div><code>{e.business_id||'workspace'}</code></div>)}<div className="activity-integrity"><ShieldCheck size={14}/>{activity.integrity.valid?'Audit integrity verified':'Audit integrity requires attention'}<span>SHA-256 hash chain</span></div></>}</section>
 </>
}
